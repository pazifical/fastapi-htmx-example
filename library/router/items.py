from typing import Annotated, Optional
from fastapi import APIRouter, Form, Request, Response, status
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
from library.classes import CreateItem, Item
from library.repository import ItemRepository
from library.service import ItemService

router = APIRouter(prefix="/api/items")

templates = Jinja2Templates(directory="templates")

repository = ItemRepository()
service = ItemService(repository)


@router.post("/", response_class=HTMLResponse)
async def add_item(
    name: Annotated[str, Form()], description: Annotated[str, Form()], request: Request
):
    try:
        service.insert(CreateItem(name=name, description=description))
    except Exception as e:
        print(e)

    return items_table(request)


@router.get("/table", response_class=HTMLResponse)
async def get_item_table(request: Request, max_items: Optional[int] = 3):
    return items_table(request, max_items)


def items_table(request: Request, max_items: Optional[int] = 3):
    return templates.TemplateResponse(
        request=request,
        name="components/item/table.html",
        context={
            "request": request,
            "items": service.find_all(limit=max_items),
            "max_items": max_items,
        },
    )


@router.get("/form", response_class=HTMLResponse)
async def get_item_form(request: Request):
    return templates.TemplateResponse(request=request, name="components/item/form.html")


@router.delete("/{item_id}")
async def delete_item(item_id: int):
    try:
        service.delete(item_id)
    except Exception as e:
        print(e)
        return Response(status_code=status.HTTP_400_BAD_REQUEST)
    return Response(status_code=status.HTTP_200_OK)


@router.get("/{item_id}/row/edit", response_class=HTMLResponse)
async def get_edit_item_row(item_id: int, request: Request):
    item = service.find_one(item_id)
    return templates.TemplateResponse(
        request=request, name="components/item/row_edit.html", context={"item": item}
    )


@router.get("/{item_id}/row", response_class=HTMLResponse)
async def get_item_row(item_id: int, request: Request):
    item = service.find_one(item_id)
    return render_item_row(item, request)


@router.put("/{item_id}/row", response_class=HTMLResponse)
async def edit_row(
    item_id: int,
    request: Request,
    name: Annotated[str, Form()],
    description: Annotated[str, Form()],
):
    item = Item(id=item_id, name=name, description=description)
    service.edit(item)
    return render_item_row(item, request)


def render_item_row(item: Item, request: Request):
    return templates.TemplateResponse(
        request=request, name="components/item/row.html", context={"item": item}
    )
