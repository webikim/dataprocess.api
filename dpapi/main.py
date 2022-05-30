from fastapi import FastAPI, Depends

from dpapi.routers import login, anno_api

app = FastAPI()

app.include_router(login.router)
app.include_router(anno_api.router)
