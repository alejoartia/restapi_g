from typing import Optional
from fastapi import FastAPI
import app.federacion_scrap as _federacion_scrap
import app.fixer_api as _fixer_api
import app.banxico_api as _banxico_api

app = FastAPI()

items_federacion = _federacion_scrap.convert_to_dict()
items_fixer = _fixer_api.currency_of_the_day()
items_banxico = _banxico_api.currency_of_the_day()

@app.get("/")
async def read_item():
    return {'rates':
            {'federacion':items_federacion,
            'fixer': items_fixer,
            'banxio': items_banxico
    }}

@app.get("/items/{item_id}")
def read_item(item_id: int, q: Optional[str] = None):
    return {"item_id": item_id, "q": q}
