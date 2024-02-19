import time
from fastapi import APIRouter, Request
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
import requests

router = APIRouter(prefix="/api/cat")

templates = Jinja2Templates(directory="templates")


@router.get("/fact/div", response_class=HTMLResponse)
async def cat_fact(request: Request):
    time.sleep(1)
    response = requests.get("https://catfact.ninja/fact")
    try:
        data = response.json()
    except Exception as e:
        print(e)
        data = {}

    return templates.TemplateResponse(
        request=request,
        name="components/cat_fact_div.html",
        context={"fact": data.get("fact")},
    )
