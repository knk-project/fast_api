from functools import wraps

from starlette.requests import Request

from core.exceptions.denied import UnauthorizedException
from roles.helpers.enum import RoleEnum


def is_admin_or_owner(func):
    @wraps(func)
    async def wrapper(request: Request, *args, **kwargs):
        user = request.user
        role = getattr(user, 'role', None)
        user_id = getattr(user, 'id', None)
        instance_id = kwargs.get('instance_id')
        if role in [RoleEnum.ADMIN] or user_id == instance_id:
            return await func(request, *args, **kwargs)

        raise UnauthorizedException()

    return wrapper
