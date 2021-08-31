from fastapi import APIRouter, Request, Depends
from fastapi.responses import HTMLResponse

from app.template_file import templates

from db.database import AsyncIOMotorClient, get_database
from db.crud import get_singleton

router = APIRouter()


@router.get('/', response_class=HTMLResponse)
async def main_page(request: Request, conn: AsyncIOMotorClient = Depends(get_database)):
    data = await get_singleton(conn, 'main_page')
    return templates.TemplateResponse('index.html',
                                      {'request': request,
                                       'page_name': data.get('page_name'),
                                       'title': data.get('title'),
                                       'text': data.get('text')})


@router.get('/contacts', response_class=HTMLResponse)
async def contacts_page(request: Request, conn: AsyncIOMotorClient = Depends(get_database)):
    data = await get_singleton(conn, 'contacts')
    context = {'request': request, 'page_name': 'Contacts'}
    if data:
        context.update(
            {'phone_number': data.get('phone_number', 'No('),
             'email': data.get('email', 'No('),
             'address': data.get('address', 'No(')
             }
        )
    return templates.TemplateResponse('contact.html', context)
