from typing import Annotated
from fastapi import FastAPI, Form, Request, Response, status
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from library.classes import CreateItem

from library.repository import ItemRepository
from library.service import ItemService


app = FastAPI()

app.mount("/static", StaticFiles(directory="static"), name="static")

templates = Jinja2Templates(directory="templates")

repository = ItemRepository()
service = ItemService(repository)


@app.get("/", response_class=HTMLResponse)
async def index(request: Request):
    return templates.TemplateResponse(request=request, name="pages/index.html")


@app.get("/api/items/add", response_class=HTMLResponse)
async def get_item_form(request: Request):
    return templates.TemplateResponse(request=request, name="components/item_form.html")


@app.delete("/api/items/{item_id}")
async def delete_item(item_id: int):
    try:
        service.delete(item_id)
    except Exception as e:
        print(e)
        return Response(status_code=status.HTTP_400_BAD_REQUEST)
    return Response(status_code=status.HTTP_200_OK)


@app.get("/api/items/add/button", response_class=HTMLResponse)
async def get_item_add_button(request: Request):
    return templates.TemplateResponse(
        request=request, name="components/item_add_button.html"
    )


@app.post("/api/items", response_class=HTMLResponse)
async def add_item(
    name: Annotated[str, Form()], description: Annotated[str, Form()], request: Request
):
    try:
        service.insert(CreateItem(name=name, description=description))
    except Exception as e:
        return templates.TemplateResponse(
            request=request,
            name="components/item_add_button.html",
            context={"message": "Error while adding new Item"},
        )

    return templates.TemplateResponse(
        request=request,
        name="components/item_add_button.html",
        context={"message": "Successfully added new Item"},
    )


@app.get("/api/items/table", response_class=HTMLResponse)
async def get_item_table(request: Request):
    return templates.TemplateResponse(
        request=request,
        name="components/item_table.html",
        context={
            "request": request,
            "items": service.find_all(),
        },
    )
