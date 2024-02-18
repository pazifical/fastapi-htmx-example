from typing import List

from library.classes import CreateItem
from library.repository import Item, ItemRepository


class ItemService:
    def __init__(self, repository: ItemRepository) -> None:
        self._repository = repository

    def delete(self, item_id: int):
        self._repository.delete(item_id)

    def find_all(self) -> List[Item]:
        return self._repository.find_all()

    def insert(self, create_item: CreateItem):
        self._repository.insert(create_item)
