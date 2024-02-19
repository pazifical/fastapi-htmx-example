from fastapi import FastAPI, Request
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
import library.router.cats as cat
import library.router.items as item
import library.router.drinks as drinks

app = FastAPI()

app.mount("/static", StaticFiles(directory="static"), name="static")
app.include_router(cat.router)
app.include_router(item.router)
app.include_router(drinks.router)

templates = Jinja2Templates(directory="templates")


@app.get("/", response_class=HTMLResponse)
async def index(request: Request):
    return templates.TemplateResponse(request=request, name="pages/index.html")
