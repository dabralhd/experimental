import logging
import requests
import json

# from cachetools import TTLCache
from project_api.globals import VESPUCCI_ENVIRONMENT

logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)

RESOURCE_API_INCLUSTER_TOKEN_DEFAULT_PATH = "/run/secrets/alloc.vespucci.st.com/serviceaccount/token"

# @cached(TTLCache(maxsize=1, ttl=60), key=lambda: "")
def alloc_token() -> str:
    with open(RESOURCE_API_INCLUSTER_TOKEN_DEFAULT_PATH, 'r') as file:
        token = file.read()
    return token

def get_efs_usage_status(userid: str):  # noqa: E501
    """get efs usage status for given user

    Return efs usage status for given user

    :rtype: bool
    """

    try:
        base_url =  f"http://resource-allocation-api.stm-vespucci-{VESPUCCI_ENVIRONMENT}-resource-allocation-api.svc.cluster.local:5004/svc/alloc/v1alpha1/resources/users/"
        headers={
            "Authorization": "Bearer " + alloc_token()
        }

        user_url = base_url + userid
        params = {'allocation': '[{"quantity": 1, "resource": "efs"}]' }
    
        r = requests.get(user_url, params=params, headers=headers)
        # logger.info(f'resource-alloc API status_code: {r.status_code}')
        if r.status_code == 200:
            r_bytes = r.content
            byte_str = r_bytes.decode('utf-8')
            json_obj = json.loads(byte_str)
            # logger.info(json_obj)
            return json_obj['items'][0]['ok']
    except Exception as e:
        logger.warning(f'- caught {type(e)}: {e}')
        raise
    return False

def is_efs_size_ok(userid: str):  # noqa: E501
    efs_size_ok = False # default value of EFS limit breached flag
    try:        
        efs_size_ok = get_efs_usage_status(userid)
        # logger.info(f'- EFS allocation status for given user: {efs_size_ok}')
    except Exception as e:
        logger.warning('- Exception occurred while accessing EFS resource allcoation.\n continuing without checking status.')
        logger.warning(f'- caught {type(e)}: {e}')

    logger.info(f'efs_size_ok: {efs_size_ok}')
    return efs_size_ok
