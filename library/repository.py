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
                id=2,
                name="Cola glas",
                description="You know where you got that from",
            ),
            3: Item(
                id=3, name="Rocks Glas", description="A glass for your next whiskey"
            ),
            4: Item(
                id=4,
                name="Blue Coffee Mug",
                description="A blue coffee mug. Nothing more.",
            ),
            5: Item(id=5, name="Water bottle", description="A bottle of water"),
        }

    def find_one(self, id: int) -> Optional[Item]:
        return self._items.get(id)

    def find_all(self, limit: Optional[int] = 3) -> List[Item]:
        items = sorted(list(self._items.values()), key=lambda x: x.id, reverse=True)
        if len(items) > limit:
            return items[:limit]
        return items

    def delete(self, id: int):
        self._items.pop(id)

    def insert(self, create_item: CreateItem):
        new_id = max(self._items.keys()) + 1
        self._items[new_id] = Item(
            id=new_id, name=create_item.name, description=create_item.name
        )

    def update(self, item: Item):
        self._items[item.id] = item
