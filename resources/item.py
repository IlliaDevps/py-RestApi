import uuid
from flask import request
from flask.views import MethodView
from flask_smorest import Blueprint, abort
#from db import items
from schemas import ItemSchema, ItemUpdateSchema

blp = Blueprint('Items', __name__, description = 'Operations with items')

@blp.route('/item/<string:item_id>')
class Item(MethodView):
    @blp.response(200, ItemSchema)
    def get(self, item_id):
        try:
            return items[item_id]
        except KeyError:
            abort(404, message= 'item not found')
    def delete(seld, item_id):
        try:
            del items[item_id]
            return {"message": "Item deleted"}
        except KeyError:
            abort(404, message= 'Item not found')   
    @blp.arguments(ItemUpdateSchema) # automatically check the JSON sent via put and validates 
    @blp.response(200, ItemSchema)
    def put(self,item_data,item_id):  #and argument decorator foes infrom of a root argument, always !!
        
        try:
            item = items[item_id]
            item |=item_data #you can also update dictionaries
            #in this way basically you merge 2 dictionaries 
            return item
        except KeyError:
            abort(404, message = "Item not found")

@blp.route('/item')
class ItemList(MethodView):
    @blp.response(200, ItemSchema(many=True)) # response a list of items
    def get(self):
        return items.values()  # when you add the decorator @blp.response(200, ItemSchema(many=True)) you will return a list of items and not an object of items
    @blp.arguments(ItemSchema) # automatically check the JSON sent via post and validates
    @blp.response(201, ItemSchema)  # this make send a response with status to clients ussing the rest API
    def post(self, item_data):
        
        #check if the item already exist
        for item in items.values():
            if(item['name']== item_data["name"] and item['store_id'] == item_data['store_id'] ):
                abort (400, message = f"Item already exist")
                
        item_id = uuid.uuid4().hex
        item = {**item_data, 'id': item_id}
        items[item_id]= item
        return item, 201