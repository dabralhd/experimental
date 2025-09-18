
import base64
import json

import flask
import jwt
import jwt.algorithms
import requests
from flask_oidc import OpenIDConnect

current_app = flask.current_app

import os

from pycognito import Cognito
from werkzeug.exceptions import Unauthorized

RSAAlgorithm = jwt.algorithms.RSAAlgorithm

class OidcProvider:

    def __init__(
        self, 
        flask_app=None,
        client_secrets_path=None
    ):
        if flask_app!=None and client_secrets_path!=None:
            self.init_app(flask_app, client_secrets_path)

    def init_app(self, flask_app, client_secrets_path):

        with flask_app.app_context():

            # Retrieve identity provider information from pre-stored configuration file.
            with open(os.path.join(client_secrets_path)) as client_secrets_file:
                print("OIDC Client parameters:")
                client_secrets = json.load(client_secrets_file)
                user_pool_id    = None
                region          = None
                client_id       = None
                realm           = None
                if "provider" not in client_secrets:
                    issuer      = client_secrets["web"]["issuer"]
                    realm       = issuer.split('/')[-1:][0]
                    provider    = "keycloak"
                elif client_secrets["provider"] == "keycloak":
                    issuer      = client_secrets["web"]["issuer"]
                    realm       = issuer.split('/')[-1:][0]
                    provider    = "keycloak"                   
                elif client_secrets["provider"] == "cognito":
                    provider    = "cognito"
                    user_pool_id= client_secrets["web"]["user_pool_id"]
                    region      = client_secrets["web"]["region"]
                    client_id   = client_secrets["web"]["client_id"]
                    if "client_secret" in client_secrets["web"]:
                        client_id_secret = client_secrets["web"]["client_secret"]
                    issuer      = f"https://cognito-idp.{region}.amazonaws.com/{user_pool_id}"
                else:
                    raise Exception("Identity provider connector not found !")
                   

            # Update Flask app configuration with identity provider information. 
            config = {
                "OIDC_OPENID_REALM":            realm,
                "OIDC_TOKEN_TYPE_HINT":         "access_token",
                "OIDC_CLIENT_SECRETS":          client_secrets_path,
                "OIDC_VALID_ISSUERS":           [ issuer ],
                "OIDC_ID_TOKEN_COOKIE_SECURE":  False,                   ## TBD
                "OIDC_REQUIRE_VERIFIED_EMAIL":  False,                   ## TBD
                "OIDC_INTROSPECTION_AUTH_METHOD": "client_secret_post",
                "OIDC_RESOURCE_SERVER_ONLY":    True,                    ## TBD
                "TESTING":                      True,
                "DEBUG":                        True
            }
            flask_app.config.update(config)
            print(config)

            # Store in current Flask app the provider type (keycloack or cognito).
            current_app.provider = provider

            # Get and store in current Flask app the OIDC/OAuth2 public keys.
            if provider == "keycloak":
                oidc = OpenIDConnect(flask_app)
                current_app.oidc = oidc
                if "certs" in client_secrets["web"]:
                    r = requests.get(client_secrets["web"]["certs"])
                else:
                    r = requests.get(issuer + "/protocol/openid-connect/certs")
                jwk_str = r.content.decode("utf-8")
                current_app.jwks = json.loads(jwk_str)["keys"]

            elif provider == "cognito":
                oidc = Cognito(user_pool_id, client_id, client_secret=client_id_secret)
                current_app.oidc = oidc
                if "certs" in client_secrets["web"]:
                    r = requests.get(client_secrets["web"]["certs"])
                else:
                    r = requests.get(issuer + "/.well-known/jwks.json")
                jwk_str = r.content.decode("utf-8")
                current_app.jwks = json.loads(jwk_str)["keys"]

            
    def authorizer(self, token):

        with current_app.app_context():
            if current_app.provider == "keycloak":
                is_authorized = current_app.oidc.validate_token(token)
                if not is_authorized:
                    raise Unauthorized()
            elif current_app.provider == "cognito":
                try:
                    current_app.oidc.access_token = token
                    current_app.oidc.check_token()
                except Exception as e:
                    print(e)
                    raise Unauthorized()
            else: 
                raise Exception("Identity provider connector not found!")
            # Decode the token and verify its signature by using related Keycloak public key
            # The JWK of the key is available at:
            # http://{keycloak_ip}:{keycloak_port}/auth/realms/{realm_name}/protocol/openid-connect/certs

            selected_jwk    = None
            token_kid       = json.loads(base64.b64decode((token.split(".")[0]) + "=="))["kid"]
            for jwk in current_app.jwks:
                if jwk["kid"] == token_kid:
                    selected_jwk = jwk
                    break

            public_key = RSAAlgorithm.from_jwk(json.dumps(selected_jwk))
            token_info = jwt.decode(token, public_key, algorithms=[selected_jwk["alg"]], options={"verify_aud": False})

            # Return the decoded token to provide protected endpoints additional information to enforce authorization policies

            # Add raw token to user object to allow calling apis on behalf of 
            # the current user
            token_info["token_string"] = token

            return token_info
