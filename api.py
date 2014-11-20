import fix_path
# then import geoffrey
from geoffrey.config import CONFIG
from geoffrey.api.server import GeoffreyApi, app, auth_wrapper

from twisted.internet import defer


class CouchDBConfigGetter(object):
    @auth_wrapper
    def get_by_api_key(self, api_key):
        raise NotImplemented

    @auth_wrapper
    def get_by_public_key(self, pkey):
        raise NotImplemented


if not CONFIG.DEBUG:
    print("NOT DEBUG")
    GeoffreyApi.config_getter = CouchDBConfigGetter()


# then start serving
API_SERVER = app.resource
