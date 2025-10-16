import logging
import requests
import json

# from cachetools import TTLCache
from project_api.globals import VESPUCCI_ENVIRONMENT

logger = logging.getLogger(__name__)
logger.setLevel(logging.ERROR)

ORGS_API_INCLUSTER_TOKEN_DEFAULT_PATH = "/run/secrets/orgs.vespucci.st.com/serviceaccount/token"

# @cached(TTLCache(maxsize=1, ttl=60), key=lambda: "")
def orgs_token() -> str:
    """Retrieve the token for accessing the orgs API."""
    logger.debug('Retrieving orgs API token...')
    try:
        with open(ORGS_API_INCLUSTER_TOKEN_DEFAULT_PATH, 'r') as file:
            token = file.read().strip()
            return token
    except Exception as e:
        logger.exception(f'Could not read token: {e}', exc_info=True)
        raise RuntimeError("Failed to retrieve orgs API token")

def check_orgs_membership(userid: str, orgid: str):  # noqa: E501
    """check if userid is member of given orgid

    Return True if user is member of given org, False otherwise

    :rtype: bool
    """
    logger.debug(f'parameters: userid={userid}, orgid={orgid}')
    try:
        # endpoint for retrieving member list: /orgs/i/{org-id}/membership
        user_url =  f"http://orgs-api.orgs-api.svc.cluster.local:5006/svc/orgs/v1alpha1/orgs/i/{orgid}/membership"  ## there is no env reference for orgs-API
        headers={
            "Authorization": "Bearer " + orgs_token()
        }

        response = requests.get(user_url, headers=headers)
        logger.debug(f'orgs API returned status_code: {response.status_code}')

        if response.status_code == 200:
            try:
                response_data = response.json()
                logger.debug(f'orgs API response: {response_data}')
                if 'items' in response_data:
                    for item in response_data['items']:
                        if item.get('user_id') == userid:
                            logger.debug(f'User {userid} is a member of org {orgid}')
                            return True, item.get('role')
                else:
                    logger.warning(f'Unexpected response structure: {response_data}')
            except json.JSONDecodeError as e:
                logger.exception(f'Failed to decode JSON response: {e}', exc_info=True)
        else:
            logger.warning(f'orgs API returned non-200 status code: {response.status_code}')
    except Exception as e:
        logger.exception(f'Exception occurred while checking membership: {e}', exc_info=True)

    logger.debug(f'User {userid} is NOT a member of org {orgid}')
    # If we reach here, the user is not a member of the org
    return False, ""

def is_user_org_member(userid: str, orgid: str) -> bool:
    """Wrapper function to check org membership."""
    try:
        return check_orgs_membership(userid, orgid)
    except Exception as e:
        logger.exception(f'Exception occurred in is_user_org_member: {e}', exc_info=True)
        return False