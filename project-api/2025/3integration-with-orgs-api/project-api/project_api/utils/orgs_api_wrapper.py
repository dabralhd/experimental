import logging
import requests
import json

# from cachetools import TTLCache
from project_api.globals import VESPUCCI_ENVIRONMENT

logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)

ORGS_API_INCLUSTER_TOKEN_DEFAULT_PATH = "/run/secrets/orgs.vespucci.st.com/serviceaccount/token"

# @cached(TTLCache(maxsize=1, ttl=60), key=lambda: "")
def orgs_token() -> str:
    logger.debug(f'> orgs_token')

    try:
        with open(ORGS_API_INCLUSTER_TOKEN_DEFAULT_PATH, 'r') as file:
            token = file.read()
    except Exception as e:
        logger.exception(f'could not read token: f{e}', exc_info=True)
        
    logger.debug(f'- token: {token}\n<')
    return token

def check_orgs_membership(userid: str, orgid: str):  # noqa: E501
    """check if userid is member of given orgid

    Return True if user is member of given org, False otherwise

    :rtype: bool
    """

    logger.debug(f'orgs API returned status_code: {r.status_code}')

    try:
        # endpoint for retrieving member list: /orgs/i/{org-id}/membership
        base_url =  f"http://orgs-api.orgs-api.svc.cluster.local:5006/svc/orgs/v1alpha1/orgs/i/{orgid}/membership"  ## there is no env reference for orgs-API
        headers={
            "Authorization": "Bearer " + orgs_token()
        }

        user_url = base_url + userid
        # params = {'OrgId': f'{orgid}' }
    
        r = requests.get(user_url, headers=headers)
        logger.debug(f'orgs API returned status_code: {r.status_code}')
        if r.status_code == 200:
            # r_bytes = r.content
            # byte_str = r_bytes.decode('utf-8')
            # json_obj = json.loads(byte_str)
            # logger.debug(json_obj)
            return False # go through the list of members returned by orgs-API and return True if membership status is ok False otherwise
    except Exception as e:
        logger.exception(f'exception occurred')
    return False

def is_user_org_member(userid: str, orgid: str):  # noqa: E501
    membership_status = False # default value of orgs membership flag
    try:        
        membership_status = check_orgs_membership(userid, orgid)
        logger.debug(f'- membership status for USER {userid} in ORG {orgid}: {membership_status}')
    except Exception as e:
        logger.exception(f'Exception occurred :{e} \n')

    logger.debug(f'membership_status: {membership_status}')
    return membership_status