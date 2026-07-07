from app.schemas.item import Item, ItemCreate, ItemUpdate


class ItemService:
    """In-memory item store.

    Swap this out for a real repository (SQLAlchemy, etc.) when a database is
    introduced — the route layer only depends on this public interface.
    """

    def __init__(self) -> None:
        self._items: dict[int, Item] = {}
        self._next_id: int = 1

    def list(self) -> list[Item]:
        return list(self._items.values())

    def get(self, item_id: int) -> Item | None:
        return self._items.get(item_id)

    def create(self, payload: ItemCreate) -> Item:
        item = Item(id=self._next_id, **payload.model_dump())
        self._items[item.id] = item
        self._next_id += 1
        return item

    def update(self, item_id: int, payload: ItemUpdate) -> Item | None:
        existing = self._items.get(item_id)
        if existing is None:
            return None
        updated = existing.model_copy(update=payload.model_dump(exclude_unset=True))
        self._items[item_id] = updated
        return updated

    def delete(self, item_id: int) -> bool:
        return self._items.pop(item_id, None) is not None


item_service = ItemService()
