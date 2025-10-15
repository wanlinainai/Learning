from typing import Union, Annotated

from fastapi import FastAPI, Query
from pydantic import BaseModel

app = FastAPI()

class Item(BaseModel):
    name: str
    description: str | None = None
    price: float
    is_offer: Union[bool, None] = None

@app.post(path="/items")
async def create_item(item: Item):
    return item

@app.post("/items/{item_id}")
async def create_item(item_id: int, item: Item):
    return {"item_id": item_id, "item": item.model_dump()}

@app.put("/items/{item_id}")
async def create_item(item_id: int, item: Item, q: str | None = None):
    result = {"item_id": item_id, **item.model_dump()}
    if q is not None:
        result.update({"q": q})
    return result

@app.get("/items")
async def get_item(q: Annotated[str | None, Query(min_length=1, max_length=10, pattern="^hahah$")] = None):
    result = {"items": [
        {"item_id": "Foo"},
        {"item_id": "Bar"}
    ]}
    if q:
        result.update({"q": q})
    return result

@app.get("/items/")
async def read_items(q: Annotated[list[str] | None, Query(description = "Query string for the items in the database",
                                                          min_length=3,
                                                          max_length=10)] = None):
    result = {"q": q}
    return result