import os
import sys

# inject so we can use our geoffrey
sys.path.insert(0, os.path.join(os.path.abspath(
                os.path.dirname('.')), "geoffrey"))


from geoffrey.config import Config
from geoffrey.api.server import GeoffreyApi, app


# now patch the config_getter
def patched_config_getter(self, request):
    return Config({"API_KEY": "yay"})


GeoffreyApi._get_config = patched_config_getter


# then start serving
API_SERVER = app.resource
