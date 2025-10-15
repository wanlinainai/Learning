from typing import Union

import uvicorn
from fastapi import FastAPI
from pydantic import BaseModel

app = FastAPI()

class Item(BaseModel):
    name: str
    price: float
    is_offer: Union[bool, None] = None

@app.get("/api/v1/read")
def read_root():
    return {"Fast-API": "read-root"}

@app.get("/api/v1/{item_id}")
def read_item(item_id: int, q: Union[int, str, None] = None):
    return {"itemInfo": item_id, "q": q}

@app.post("/api/v1/{item_id}")
def update_item(item_id: int, item: Item):
    return {"item_name": item.name, "item_id": item_id}

if __name__ == '__main__':
    uvicorn.run(app, host='127.0.0.1', port=888)