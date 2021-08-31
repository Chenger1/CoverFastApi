from fastapi import APIRouter, Request, Depends, HTTPException
from fastapi.responses import HTMLResponse, RedirectResponse

from app.template_file import templates

from dependencies import check_is_authenticated
from db.database import AsyncIOMotorClient, get_database
from db.schema import MainPageSchema, UserSchema, CreateUserSchema, ContactsSchema
from db import crud


router = APIRouter(
    prefix='/admin',
    tags=['admin'],
    dependencies=[Depends(check_is_authenticated)]
)


@router.get('/', response_class=HTMLResponse)
async def admin_page(request: Request, conn: AsyncIOMotorClient = Depends(get_database)):
    instance = await crud.get_singleton(conn, 'main_page')
    return templates.TemplateResponse('/admin/main_page.html', {'request': request,
                                                                'page_name': instance.get('page_name'),
                                                                'title': instance.get('title'),
                                                                'text': instance.get('text')})


@router.post('/')
async def main_page(request: Request, data: MainPageSchema,
                    conn: AsyncIOMotorClient = Depends(get_database)):
    result = await crud.update_singleton(conn, data.dict(), 'main_page')
    return {'status': 200 if result else 404}


@router.get('/users')
async def users_page(request: Request, conn: AsyncIOMotorClient = Depends(get_database)):
    instances = await crud.retrieve_from_collections(conn, 'user')
    return templates.TemplateResponse('/admin/users_page.html', {'request': request,
                                                                 'instances': instances})


@router.get('/users/add_user', response_class=HTMLResponse)
async def add_user_page(request: Request):
    return templates.TemplateResponse('admin/add_user.html', {'request': request})


@router.post('/users/add_user')
async def add_user_post(request: Request, data: CreateUserSchema, conn: AsyncIOMotorClient = Depends(get_database)):
    result = await crud.create_new_item(conn, 'user', data.dict())
    return {'status_code': 200 if result else 404}


@router.get('/users/{id}')
async def user_detail(id: str, request: Request, conn: AsyncIOMotorClient = Depends(get_database)):
    instance = await crud.retrieve_data(conn, id, 'user')
    if not str(instance.get('_id')) == request.session.get('user')['id']:
        raise HTTPException(status_code=404,
                            detail='You don`t have access to this user')
    return templates.TemplateResponse('/admin/user_detail_page.html', {'request': request,
                                                                       '_id': str(instance.get('_id')),
                                                                       'email': instance.get('email'),
                                                                       'username': instance.get('username')})


@router.patch('/users/{id}')
async def change_user_info(id: str, request: Request, data: UserSchema,
                           conn: AsyncIOMotorClient = Depends(get_database)):
    current_user = request.session.get('user')
    result = await crud.update_item(conn, id, 'user', data.dict())
    if result:
        #  Update session
        current_user['username'] = data.username
        current_user['email'] = data.email
        request.session.pop('user')
        request.session['user'] = current_user
    return {'status_code': 200 if result else 404}


@router.get('/users/{id}/delete')
async def delete_user(id: str, request: Request, conn: AsyncIOMotorClient = Depends(get_database)):
    if id != request.session.get('user_id')['user_id']:
        raise HTTPException(status_code=404,
                            detail='You don`t have access to this user')
    await crud.delete_item(conn, id, 'user')
    return RedirectResponse('/admin/users', status_code=303)


@router.get('/contacts', response_class=HTMLResponse)
async def edit_contacts_page(request: Request, conn: AsyncIOMotorClient = Depends(get_database)):
    data = await crud.get_singleton(conn, 'contacts')
    context = {'request': request}
    if data:
        context.update(
            {'phone_number': data.get('phone_number'),
             'email': data.get('email'),
             'address': data.get('address')
             }
        )
    return templates.TemplateResponse('admin/edit_contacts.html', context)


@router.post('/contacts')
async def edit_contacts(request: Request, data: ContactsSchema,
                        conn: AsyncIOMotorClient = Depends(get_database)):
    result = await crud.update_singleton(conn, data.dict(), 'contacts')
    return {'status_code': 200 if result else 404}
