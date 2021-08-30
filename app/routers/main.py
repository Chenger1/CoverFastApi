from fastapi import APIRouter, Request, Depends
from fastapi.responses import HTMLResponse

from app.template_file import templates

from db.database import AsyncIOMotorClient, get_database
from db.crud import get_main_page

router = APIRouter()


@router.get('/', response_class=HTMLResponse)
async def main_page(request: Request, conn: AsyncIOMotorClient = Depends(get_database)):
    data = await get_main_page(conn)
    return templates.TemplateResponse('index.html',
                                      {'request': request,
                                       'page_name': data.get('page_name'),
                                       'title': data.get('title'),
                                       'text': data.get('text')})
