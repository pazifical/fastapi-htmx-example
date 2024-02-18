from typing import Dict, List, Optional
from library.classes import Item, CreateItem


class ItemRepository:
    def __init__(self) -> None:
        self._items: Dict[int,] = {
            0: Item(
                id=0, name="Coffee Mug", description="An artisticly forged coffee mug"
            ),
            1: Item(
                id=1, name="Teapot", description="A teapot made out of purple ceramics"
            ),
            2: Item(
                id=2, name="Rocks Glas", description="A glass for your next whiskey"
            ),
        }

    def find_one(self, id: int) -> Optional[Item]:
        return self._items.get(id)

    def find_all(self) -> List[Item]:
        return list(self._items.values())

    def delete(self, id: int):
        self._items.pop(id)

    def insert(self, create_item: CreateItem):
        new_id = max(self._items.keys()) + 1
        self._items[new_id] = Item(
            id=new_id, name=create_item.name, description=create_item.name
        )

    def update(self, item: Item):
        self._items[item.id] = item
