import os

from fastapi import Request, APIRouter
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates

path = os.path.dirname(os.path.abspath(__file__))

router = APIRouter()
templates = Jinja2Templates(directory=os.path.join(path, '../templates'))


@router.get("/", response_class=HTMLResponse)
async def home(request: Request):
    return templates.TemplateResponse("index.html", {"request": request})
