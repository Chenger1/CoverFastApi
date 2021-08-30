from fastapi import APIRouter, Request, Depends, HTTPException
from fastapi.responses import HTMLResponse

from app.template_file import templates

from dependencies import check_is_authenticated
from db.database import AsyncIOMotorClient, get_database
from db.schema import MainPageSchema, UserSchema
from db import crud


router = APIRouter(
    prefix='/admin',
    tags=['admin'],
    dependencies=[Depends(check_is_authenticated)]
)


@router.get('/', response_class=HTMLResponse)
async def admin_page(request: Request, conn: AsyncIOMotorClient = Depends(get_database)):
    instance = await crud.get_main_page(conn)
    return templates.TemplateResponse('/admin/main_page.html', {'request': request,
                                                                'page_name': instance.get('page_name'),
                                                                'title': instance.get('title'),
                                                                'text': instance.get('text')})


@router.post('/')
async def main_page(request: Request, data: MainPageSchema,
                    conn: AsyncIOMotorClient = Depends(get_database)):
    result = await crud.update_main_page(conn, data.dict())
    return {'status': 200 if result else 404}


@router.get('/users')
async def users_page(request: Request, conn: AsyncIOMotorClient = Depends(get_database)):
    instances = await crud.retrieve_from_collections(conn, 'user')
    return templates.TemplateResponse('/admin/users_page.html', {'request': request,
                                                                 'instances': instances})


@router.get('/users/{id}')
async def user_detail(id: str, request: Request, conn: AsyncIOMotorClient = Depends(get_database)):
    instance = await crud.retrieve_data(conn, id, 'user')
    if not instance.get('username') == request.session.get('user')['username']:
        raise HTTPException(status_code=404,
                            detail='You don`t have access to this uer')
    return templates.TemplateResponse('/admin/user_detail_page.html', {'request': request,
                                                                       '_id': str(instance.get('_id')),
                                                                       'email': instance.get('email'),
                                                                       'username': instance.get('username')})


@router.patch('/users/{id}')
async def change_user_info(id: str, request: Request, data: UserSchema,
                           conn: AsyncIOMotorClient = Depends(get_database)):
    result = await crud.update_item(conn, id, 'user', data.dict())
    return {'status_code': 200 if result else 404}
