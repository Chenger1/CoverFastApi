from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles

from starlette.middleware.sessions import SessionMiddleware

from routers import main, admin
from authentication import router as auth_router
from config import SECRET_KEY

import uvicorn

from db.database import connect_to_db, close_connection


app = FastAPI()
app.include_router(auth_router)
app.include_router(main.router)
app.include_router(admin.router)

app.mount('/static', StaticFiles(directory='static'), name='static')
app.add_middleware(SessionMiddleware, **{'secret_key': SECRET_KEY})

session = SessionMiddleware(app, SECRET_KEY)

app.add_event_handler('startup', connect_to_db)
app.add_event_handler('shutdown', close_connection)


if __name__ == '__main__':
    uvicorn.run(app, host='127.0.0.1', port=8000)
