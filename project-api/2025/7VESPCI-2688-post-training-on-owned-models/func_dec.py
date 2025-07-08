from functools import wraps
import connexion
from flask import Response
from project_api.utils.orgs_api_wrapper import(is_user_org_member)
from project_api.utils.error_types import (client_side_error, ErrorType)
import logging

logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)

def with_effective_user_id(func):
    @wraps(func)
    def wrapper(user, *args, **kwargs):
        as_org = connexion.request.args.get('as_org')
        effective_user_id = user
        if as_org:
            if is_user_org_member(user, as_org):
                effective_user_id = as_org
            else:
                logger.error(f'user {user} is not a member of org {as_org}')
                return Response(status=client_side_error(ErrorType.FORBIDDEN))
        # Pass effective_user_id to the view functiond
        return func(user, *args, effective_user_id=effective_user_id, **kwargs)
    return wrapper
