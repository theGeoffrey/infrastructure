import fix_path

from klein.app import Klein
from twisted.web.static import File
from twisted.web import proxy
from twisted.internet.defer import inlineCallbacks, returnValue
from txDiscourse import DiscourseClient
from geoffrey.config import CONFIG
from geoffrey.helpers import get_database_connection
from geoffrey.api.server import app as api_server

import json
import uuid


class GeoffreyService(Klein):
    pass


app = GeoffreyService()


VALIDATION_FUNC = """
  function(newDoc, oldDoc, userCtx, secObj) {
      if ((newDoc._id === "CONFIG") && (newDoc._deleted === true) && (userCtx.roles.indexOf('_admin') === -1)){
              throw({forbidden: 'Only admins may delete Config objects.'});
      }
  }
"""


@app.route("/api/create_new_instance")
@inlineCallbacks
def new_instance(request):
    users_db = get_database_connection("_users")

    # Query to make sure we have access
    yield users_db.infoDB()

    dc_url = request.args['dc_url'][0]
    api_key = request.args['api_key'][0]
    username = "system"

    try:
        # set if given
        username = request.args["username"][0]
    except KeyError:
        pass

    # check if we can connect to the admin site with the settings
    client = DiscourseClient(dc_url, api_key, username)

    yield client.request('GET', '/admin/site_settings.json')

    new_db_name = "geoffrey-" + uuid.uuid4().hex
    new_user = uuid.uuid4().hex
    new_password = uuid.uuid4().hex

    yield users_db.put("org.couchdb.user:" + new_user,
                       data=json.dumps({"name": new_user,
                                        "roles": ['geoffrey-user'],
                                        "type": "user",
                                        "password": new_password
                                        }))

    new_db = get_database_connection(new_db_name)
    yield new_db.createDB()

    yield new_db.put("_design/_auth",
                     data=json.dumps({"language": "javascript",
                                      "validate_doc_update": VALIDATION_FUNC}))


    security_config = json.dumps({"admins": {"names": [CONFIG.COUCH_USER],
                                             "roles": ["admins"]},
                                  "members": {"names": [new_user],
                                              "roles": ["workers"]}
                                  })

    yield new_db.put("/_security", data=security_config)

    # We could potentially set up continuous replication, too
    yield new_db.put("CONFIG", data=json.dumps({
        "dc_key": api_key,
        "dc_user": username,
        "dc_url": dc_url,
        "enabled_services": [],
        "apps": {}
        }))

    returnValue(json.dumps({"api_key": "{}:{}@{}".format(new_user,
                            new_password, new_db_name),
                            "public_key": new_db_name}))


@app.route('/api/', branch=True)
def api(request):
    return api_server.resource()


@app.route("/server_config.js")
def config(request):
    return "window.GEOF_CONFIG = {}".format(
           json.dumps(api_server.get_server_settings()))


if CONFIG.DEBUG:

    @app.route('/assets/', branch=True)
    def assets(request):
        return proxy.ReverseProxyResource('localhost', 8092, '/assets')

    @app.route("/assets_promo/", branch=True)
    def assets_promo(request):
        return proxy.ReverseProxyResource('localhost', 8093, '/assets')

    @app.route('/dashboard/', branch=False)
    def dashboard(request):
        return proxy.ReverseProxyResource('localhost', 8092, '')

    @app.route("/", branch=False)
    def promo(request):
        return proxy.ReverseProxyResource('localhost', 8093, '')
else:

    @app.route('/assets/', branch=True)
    def assets(request):
        return File('./geoffrey/ui/dist/assets/')

    @app.route("/assets_promo/", branch=True)
    def assets_promo(request):
        return File('./promo/dist/assets/')

    @app.route('/dashboard/', branch=False)
    def dashboard(request):
        return File('./geoffrey/ui/dist/')

    @app.route("/", branch=False)
    def promo(request):
        return File('./promo/dist/')

resource = app.resource
