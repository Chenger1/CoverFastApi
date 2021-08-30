from fastapi import APIRouter, Request
from fastapi.responses import HTMLResponse

from app.template_file import templates

router = APIRouter()


@router.get('/', response_class=HTMLResponse)
async def main_page(request: Request):
    return templates.TemplateResponse('index.html',
                                      {'request': request})
