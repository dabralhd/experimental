
import logging

import project_api.globals as globs
from project_api.globals import OIDC_CLIENT_SECRETS_PATH, GlobalObjects
from project_api.utils.patched_flask_oidc_provider import OidcProvider

# from flask_oidc_provider import OidcProvider



"""
controller generated to handled auth operation described at:
https://connexion.readthedocs.io/en/latest/security.html
"""

def check_bearerAuth(token):
    if globs.FLASK_ENV == 'development' and globs.KUBERNETES_SERVICE_PORT_HTTPS == None:
        dummy = {
            "sub": "00000000-0000-0000-0000-000000000000",
            # Dummy token
            "token_string": "dummy"
        }
        return dummy
    try:
        oidc_provider = OidcProvider()
        oidc_provider.init_app(GlobalObjects.getInstance().flask_app, OIDC_CLIENT_SECRETS_PATH)
        user = OidcProvider().authorizer(token)        
        return user 
    except Exception as e:
        logging.exception(e)
        raise e
