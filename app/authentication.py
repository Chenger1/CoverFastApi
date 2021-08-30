from fastapi import APIRouter, Request, Depends
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from fastapi.responses import HTMLResponse, RedirectResponse

from passlib.context import CryptContext
from app.template_file import templates

from db.crud import get_user_by_email
from db.database import AsyncIOMotorClient, get_database

router = APIRouter(
    prefix='/login',
    tags=['login']
)

ALGORITHM = 'HS256'
ACCESS_TOKEN_EXPIRE_MINUTES = 180

oauth2_scheme = OAuth2PasswordBearer(tokenUrl='login')

pwd_context = CryptContext(schemes=['bcrypt'], deprecated='auto')


def verify_password(plain_password: str, hashed_password: str) -> bool:
    return pwd_context.verify(plain_password, hashed_password)


def get_password_hash(plain_password: str) -> str:
    return pwd_context.hash(plain_password)


async def authenticate_user(email: str, password: str, conn: AsyncIOMotorClient):
    user = await get_user_by_email(conn, email)
    if not user:
        return False
    if not verify_password(password, user.password):
        return False
    return user


@router.get('/', response_class=HTMLResponse)
async def login_page(request: Request):
    return templates.TemplateResponse('login.html', {'request': request})


@router.post('/', response_class=HTMLResponse)
async def login(request: Request, form_data: OAuth2PasswordRequestForm = Depends(),
                conn: AsyncIOMotorClient = Depends(get_database)):
    user = await authenticate_user(form_data.username, form_data.password, conn)
    if not user:
        return templates.TemplateResponse('login.html', {'request': request,
                                                         'error': 'Wrong username or password',
                                                         'username': form_data.username,
                                                         'password': form_data.password})
    request.session.update({'user': user.dict()})
    return RedirectResponse('/admin/', status_code=303)
