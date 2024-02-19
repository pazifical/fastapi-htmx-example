import time
from typing import Annotated
from fastapi import FastAPI, Form, Request, Response, status
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
import requests
from library.classes import CreateItem, Item

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


@app.get("/api/cat/fact/div", response_class=HTMLResponse)
async def index(request: Request):
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


@app.get("/api/items/add", response_class=HTMLResponse)
async def get_item_form(request: Request):
    return templates.TemplateResponse(request=request, name="components/item_form.html")


@app.get("/api/items/{item_id}/edit", response_class=HTMLResponse)
async def get_edit_row(item_id: int, request: Request):
    item = service.find_one(item_id)
    # TODO: Implement: Open a modal!
    # print(item)
    # return templates.TemplateResponse(
    #     request=request,
    #     name="components/item_table_edit_row.html",
    #     context={"item": item},
    # )


@app.delete("/api/items/{item_id}")
async def delete_item(item_id: int):
    try:
        service.delete(item_id)
    except Exception as e:
        print(e)
        return Response(status_code=status.HTTP_400_BAD_REQUEST)
    return Response(status_code=status.HTTP_200_OK)


@app.put("/api/items/row", response_class=HTMLResponse)
async def edit_item(
    id: Annotated[int, Form()],
    name: Annotated[str, Form()],
    description: Annotated[str, Form()],
    request: Request,
):
    service.edit(Item(id=id, name=name, description=description))
    return templates.TemplateResponse(
        request=request,
        name="components/item_table.html",
        context={"request": request, "items": service.find_all()},
    )


@app.post("/api/items", response_class=HTMLResponse)
async def add_item(
    name: Annotated[str, Form()], description: Annotated[str, Form()], request: Request
):
    message = ""
    try:
        service.insert(CreateItem(name=name, description=description))
    except Exception as e:
        message = "ERROR"

    return templates.TemplateResponse(
        request=request,
        name="components/item_table.html",
        context={"request": request, "items": service.find_all(), "message": message},
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
