import os

from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles

from dpapi.routers import login, anno_api, dp_api, web

root_path = os.path.dirname(os.path.abspath(__file__))

app = FastAPI()

app.include_router(login.router)
app.include_router(dp_api.router)
app.include_router(anno_api.router)

app.include_router(web.router)

app.mount("/static", StaticFiles(directory=os.path.join(root_path, 'static')), name="static")
