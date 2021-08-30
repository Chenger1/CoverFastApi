from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles

from routers import main

import uvicorn

app = FastAPI()
app.include_router(main.router)

app.mount('/static', StaticFiles(directory='static'), name='static')


if __name__ == '__main__':
    uvicorn.run(app, host='127.0.0.1', port=8000)
