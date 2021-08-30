from fastapi import APIRouter, Request, Depends
from fastapi.responses import HTMLResponse

from app.template_file import templates

from dependencies import check_is_authenticated
from db.database import AsyncIOMotorClient, get_database
from db.schema import MainPageSchema
from db.crud import update_main_page


router = APIRouter(
    prefix='/admin',
    tags=['admin'],
    dependencies=[Depends(check_is_authenticated)]
)


@router.get('/', response_class=HTMLResponse)
async def admin_page(request: Request):
    return templates.TemplateResponse('/admin/main_page.html', {'request': request})


@router.post('/')
async def main_page(request: Request, data: MainPageSchema,
                    conn: AsyncIOMotorClient = Depends(get_database)):
    result = await update_main_page(conn, data.dict())
    return {'status': 200 if result else 404}
