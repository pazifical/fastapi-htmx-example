from typing import Annotated
from fastapi import APIRouter, Form, Request
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates

router = APIRouter(prefix="/api/drinks")

templates = Jinja2Templates(directory="templates")

drinks = ["🍺 Beer", "🍷 Wine", "🥃 Whiskey", "🍹 Cocktail"]

selected_drink = ""


@router.get("/", response_class=HTMLResponse)
async def get_drink_selector(request: Request):
    return templates.TemplateResponse(
        request=request,
        name="components/drink_selector.html",
        context={"request": request, "options": drinks, "selected": selected_drink},
    )


@router.put("/", response_class=HTMLResponse)
async def update_drink(request: Request, drink: Annotated[str, Form()]):
    global selected_drink
    selected_drink = drink
    return await get_drink_selector(request)
