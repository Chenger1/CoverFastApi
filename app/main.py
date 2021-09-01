from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles

from starlette.middleware.sessions import SessionMiddleware

from .routers import main, admin
from .authentication import router as auth_router
from .config import SECRET_KEY

import uvicorn

from .db.database import connect_to_db, close_connection
from .utils.exceptions import (unauthorized_exception_handler, http_exception_handler, UnauthorizedException,
                              StarletteHTTPException)


app = FastAPI()
app.include_router(auth_router)
app.include_router(main.router)
app.include_router(admin.router)

try:
    app.mount('/static', StaticFiles(directory='static'), name='static')
except RuntimeError:
    app.mount('/static', StaticFiles(directory='app/static'), name='static')  # For Docker
     
app.add_middleware(SessionMiddleware, **{'secret_key': SECRET_KEY})

session = SessionMiddleware(app, SECRET_KEY)

app.add_event_handler('startup', connect_to_db)
app.add_event_handler('shutdown', close_connection)
app.add_exception_handler(UnauthorizedException, unauthorized_exception_handler)
app.add_exception_handler(StarletteHTTPException, http_exception_handler)


if __name__ == '__main__':
    uvicorn.run(app, host='127.0.0.1', port=8000)
