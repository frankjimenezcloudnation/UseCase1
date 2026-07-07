from fastapi import APIRouter, HTTPException, status

from app.schemas.item import Item, ItemCreate, ItemUpdate
from app.services.item_service import item_service

router = APIRouter()


@router.get("", response_model=list[Item])
def list_items() -> list[Item]:
    return item_service.list()


@router.post("", response_model=Item, status_code=status.HTTP_201_CREATED)
def create_item(payload: ItemCreate) -> Item:
    return item_service.create(payload)


@router.get("/{item_id}", response_model=Item)
def get_item(item_id: int) -> Item:
    item = item_service.get(item_id)
    if item is None:
        raise HTTPException(status_code=404, detail="Item not found")
    return item


@router.put("/{item_id}", response_model=Item)
def update_item(item_id: int, payload: ItemUpdate) -> Item:
    item = item_service.update(item_id, payload)
    if item is None:
        raise HTTPException(status_code=404, detail="Item not found")
    return item


@router.delete("/{item_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_item(item_id: int) -> None:
    if not item_service.delete(item_id):
        raise HTTPException(status_code=404, detail="Item not found")
