from fastapi import APIRouter, Request, Depends
from fastapi.responses import HTMLResponse

from app.template_file import templates

from dependencies import check_is_authenticated


router = APIRouter(
    prefix='/admin',
    tags=['admin'],
    dependencies=[Depends(check_is_authenticated)]
)


@router.get('/', response_class=HTMLResponse)
async def admin_page(request: Request):
    return templates.TemplateResponse('/admin/admin_index.html', {'request': request})
