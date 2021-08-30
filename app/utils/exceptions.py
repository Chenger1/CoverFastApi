from fastapi import Request
from fastapi.responses import RedirectResponse


class UnauthorizedException(Exception):
    pass


async def unauthorized_exception_handler(request: Request, exc: UnauthorizedException):
    return RedirectResponse(url='/', status_code=303)
