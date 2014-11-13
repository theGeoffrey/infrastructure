import fix_path
# then import geoffrey
from geoffrey.config import Config
from geoffrey.api.server import GeoffreyApi, app

from twisted.internet import defer


# now patch the config_getter
def patched_config_getter(self, request):
    request.config = Config({"api_key": "yay",
                             "enabled_services": ["mailchimp_subscribe"],
                             "apps":
                             {"mailchimp":
                              {"API_KEY":
                               "4f34ea944dd1e33a5452550789042f9c-us9",
                               "DATA_CENTER": "us9",
                               "TEST_LIST_ID": "f4b255a33a"}}})

    return defer.succeed(request)


GeoffreyApi._get_config = patched_config_getter

# then start serving
API_SERVER = app.resource
