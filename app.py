import sys
import uuid
from datetime import datetime
from flask import Flask, request
from db import items,stores
from flask_smorest import abort



now = datetime.now()
message = f'{now:date %d:%m:%y: time : %H:%M:%S} Running and Logged!'
print(message, file = sys.stderr)
with open ('logs.txt', 'a') as file:
    print(message, file=file)

#---------------------------------------------------


app = Flask (__name__)

@app.get("/store")
def get_stores():
    return {'stores':list(stores.values()) }

@app.get("/store/<string:store_id>/")
def get_specific_store(store_id):
    try:
        return stores[store_id],201
    except KeyError:
        abort(404, message= 'Store not found')

@app.post("/store")
def create_stores():
    store_data = request.get_json()
    store_id = uuid.uuid4().hex
    if ("name" not in store_data):
        abort(400,"Bad request, ensure 'name' is included in the JSON playload")
    for store in stores.values():
        if(store_data['name']==store['name']):
            abort (400, message = "Store already exist")
    store = {**store_data, 'id': store_id}
    stores[store_id]=  store #not more a list is a dictionary stores.append(new_store)
    return store, 201

@app.delete('/store/<string:store_id>')
def delete_item(store_id):
    try:
        del stores[store_id]
        return {"message": "Store deleted"}
    except KeyError:
        abort(404, message= 'Store not found')
#---------------------------Items----------------------------------------
@app.get('/item')
def get_all_items():
     return {'items':list(items.values())}

@app.get('/item/<string:item_id>')
def get_item(item_id):
    try:
        return items[item_id]
    except KeyError:
        abort(404, message= 'item not found')

@app.post('/item')
def create_item():
    item_data = request.get_json()
    if ("price" not in item_data 
        or "store_id" not in item_data 
        or "name" not in item_data):
        abort (
            400, message = f"Bad request. Ensure 'price' , 'store_id' , 'name' are include in the JSON payload. "
        )
    #check if the item already exist
    for item in items.values():
        if(item['name']== item_data["name"] and item['store_id'] == item_data['store_id'] ):
            abort (400, message = f"Item already exist")

    if item_data['store_id'] not in stores:
            abort(404, message= 'Store not found')
            
    item_id = uuid.uuid4().hex
    item = {**item_data, 'id': item_id}
    items[item_id]= item
    return item, 201

@app.delete('/item/<string:item_id>')
def delete_item(item_id):
    try:
        del items[item_id]
        return {"message": "Item deleted"}
    except KeyError:
        abort(404, message= 'Item not found')

@app.put('/item/<string:item_id>')
def update_item(item_id):
    item_data = request.get_json()
    if ("price" not in item_data or "name" not in item_data ):
        abort(400, message = "Bad request. Ensure 'price', and 'name' are included in the JSON payload")
    try:
        item = items[item_id]
        item |=item_data #you can also update dictionaries
        #in this way basically you merge 2 dictionaries 

        return item
    except KeyError:
        abort(404, message = "Item not found")





    

