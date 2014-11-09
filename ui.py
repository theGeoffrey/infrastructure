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

EXT_CONFIG = json.dumps({
    "API_ENDPOINT": CONFIG.API_ENDPOINT
})


@app.route("/anouk")
def anouk(request):
    return '<img src="http://media.giphy.com/media/pE1u2Ov7eYF68/giphy.gif">'


@app.route("/")
def promo(request):
    return File('./static/index.html')


@app.route("/dashboard")
def dashboard(request):
    return File('./static/dashboard.html')


@app.route("/config.json")
def config(request):
    return EXT_CONFIG


@app.route('/api/', branch=True)
def api(request):
    return api_server


@app.route('/static/', branch=True)
def statics(request):
    return File('./static/')


WEB_UI = app.resource
