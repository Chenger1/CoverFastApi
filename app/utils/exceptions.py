from fastapi import Request
from fastapi.responses import RedirectResponse
from fastapi.exceptions import StarletteHTTPException

from template_file import templates


class UnauthorizedException(Exception):
    pass


async def unauthorized_exception_handler(request: Request, exc: UnauthorizedException):
    return RedirectResponse(url='/', status_code=303)


async def http_exception_handler(request: Request, exc: StarletteHTTPException):
    return templates.TemplateResponse('error.html', {'request': request,
                                                     'detail': exc.detail,
                                                     'code': exc.status_code})
