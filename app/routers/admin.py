from fastapi import APIRouter, Request
from fastapi.responses import HTMLResponse

from app.template_file import templates


router = APIRouter(
    prefix='/admin',
    tags=['admin']
)


@router.get('/', response_class=HTMLResponse)
async def admin_page(request: Request):
    return templates.TemplateResponse('/admin/admin_index.html', {'request': request})
