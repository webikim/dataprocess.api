from fastapi import FastAPI, Depends

from dpapi.routers import login

app = FastAPI()

app.include_router(login.router)

