from fastapi import FastAPI, Request, Response
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from pydantic import BaseModel


class Item(BaseModel):
    id: int
    name: str
    description: str


ITEMS = [
    Item(id=0, name="Coffee Mug", description="An artisticly forged coffee mug"),
    Item(id=1, name="Teapot", description="A teapot made out of purple ceramics"),
    Item(id=2, name="Rocks Glas", description="A glass for your next whiskey"),
]


app = FastAPI()

app.mount("/static", StaticFiles(directory="static"), name="static")

templates = Jinja2Templates(directory="templates")


@app.get("/", response_class=HTMLResponse)
async def index(request: Request):
    return templates.TemplateResponse(request=request, name="pages/index.html")


@app.delete("/api/items/{item_id}")
async def delete_item(item_id: int):
    print(item_id)
    return Response(status_code=200)


@app.get("/api/items/table", response_class=HTMLResponse)
async def get_item_table(request: Request):
    return templates.TemplateResponse(
        request=request,
        name="components/item_table.html",
        context={
            "request": request,
            "items": ITEMS,
        },
    )
