# Run:
# (to open) flask run
# (close)   ctrl+C

# Run continuously with docker:
# (as daemon)   docker run -dp 5000:5000 -w //app -v "$(Get-Location)://app" flask-smorest-api
# (in terminal) docker run -p 5000:5000 -w //app -v "$(Get-Location)://app" flask-smorest-api
# (to see id)   docker container ls
# (to kill)     docker container kill <container-id>

import uuid
from flask import Flask, request
from flask_smorest import abort
from db import stores, items

app = Flask(__name__)

# ----------------- STORES --------------------


@app.get("/store")  # http://127.0.0.1:5000/store
def get_stores():
    return {"stores": list(stores.values())}


@app.get("/store/<string:store_id>")
def get_store(store_id):
    try:
        return stores[store_id]
    except KeyError:
        abort(404, message="Store not found")


@app.post("/store")  # http://127.0.0.1:5000/store
def create_store():
    store_data = request.get_json()
    store_id = uuid.uuid4().hex
    store = {**store_data, "id": store_id}  # pasamos todas las weas del dict
    stores[store_id] = store
    return store, 201


@app.delete("/store/<string:store_id>")
def delete_store(store_id):
    try:
        del stores[store_id]
        return {"message": "Store deleted"}
    except KeyError:
        abort(404, message="Store not found")


@app.put("/store/<string:store_id>")
def update_store(store_id):
    store_data = request.get_json()
    try:
        store = stores[store_id]
        store |= store_data  # que buena forma!
        return store
    except KeyError:
        abort(404, message="Store not found")


# --------------------- ITEMS -------------------------


@app.get("/item/<string:item_id>")
def get_item(item_id):
    try:
        return items[item_id]
    except KeyError:
        abort(404, message="Item not found")


@app.get("/item")
def get_all_items():
    return {"items": list(items.values())}


@app.post("/item")
def create_item(name):
    item_data = request.get_json()
    if item_data["store_id"] not in stores:
        abort(404, message="Store not found")

    item_id = uuid.uuid4().hex
    item = {**item_data, "id": item_id}  # pasamos todas las weas del dict
    items[item_id] = item

    return item, 201


@app.delete("/item/<string:item_id>")
def delete_item(item_id):
    try:
        del items[item_id]
        return {"message": "Item deleted"}
    except KeyError:
        abort(404, message="Item not found")


@app.put("/item/<string:item_id>")
def update_item(item_id):
    item_data = request.get_json()
    try:
        item = items[item_id]
        item |= item_data  # que buena forma!
        return item
    except KeyError:
        abort(404, message="Item not found")
