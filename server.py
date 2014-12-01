import fix_path
from klein.app import Klein
from twisted.web.static import File
from geoffrey.config import CONFIG
from api import API_SERVER

import json


class GeoffreyUI(Klein):
    pass


app = GeoffreyUI()
api_server = API_SERVER()


@app.route("/")
def promo(request):
    return File('./static/index.html')


@app.route('/api/', branch=True)
def api(request):
    return api_server


@app.route('/ui/', branch=True)
def statics(request):
    return File('./geoffrey/ui/dist/')


resource = app.resource

