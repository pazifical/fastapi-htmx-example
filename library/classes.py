from pydantic import BaseModel


class CreateItem(BaseModel):
    name: str
    description: str


class Item(BaseModel):
    id: int
    name: str
    description: str
