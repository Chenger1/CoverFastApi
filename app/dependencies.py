from fastapi import Request

from app.utils.exceptions import UnauthorizedException


def check_is_authenticated(request: Request):
    user = request.session.get('user')
    if not user or not user.get('is_admin'):
        raise UnauthorizedException
