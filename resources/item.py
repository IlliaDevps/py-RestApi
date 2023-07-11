import uuid
from flask import request
from flask.views import MethodView
from flask_smorest import Blueprint, abort
from sqlalchemy.exc import SQLAlchemyError

from db import db
from models import ItemModel
from schemas import ItemSchema, ItemUpdateSchema



blp = Blueprint('Items', __name__, description = 'Operations with items')

@blp.route('/item/<string:item_id>')
class Item(MethodView):
    @blp.response(200, ItemSchema)
    def get(self, item_id):
        item = ItemModel.query.get_or_404(item_id)
        return item
        '''try:  # do not need this anymore
            return items[item_id]
        except KeyError:
            abort(404, message= 'item not found')''' 
    def delete(seld, item_id):
       item = ItemModel.query.get_or_404(item_id)
       db.session.delete(item)
       db.session.commit()
       return {'message': 'Item deleted.'}, 200
       ''' try:
            del items[item_id]
            return {"message": "Item deleted"}
        except KeyError:
            abort(404, message= 'Item not found')   '''
    @blp.arguments(ItemUpdateSchema) # automatically check the JSON sent via put and validates 
    @blp.response(200, ItemSchema)
    def put(self,item_data, item_id):  #and argument decorator foes infrom of a root argument, always !!
        item = ItemModel.query.get(item_id)
        if item:
            item.price = item_data['price']
            item.name = item_data['name']
        else: 
            item = ItemModel(id= item_id, **item_data)

        db.session.add(item)
        db.session.commit()

        return item
    
        #raise NotImplementedError("Updating an item is not implemented")
        '''try:
            item = items[item_id]
            item |=item_data #you can also update dictionaries merge update dictionary
            #in this way basically you merge 2 dictionaries 
            return item
        except KeyError:
            abort(404, message = "Item not found")'''

@blp.route('/item')
class ItemList(MethodView):
    @blp.response(200, ItemSchema(many=True)) # response a list of items
    def get(self):
        return ItemModel.query.all()
        #return items.values()  # when you add the decorator @blp.response(200, ItemSchema(many=True)) you will return a list of items and not an object of items
    @blp.arguments(ItemSchema) # automatically check the JSON sent via post and validates
    @blp.response(201, ItemSchema)  # this make send a response with status to clients ussing the rest API
    def post(self, item_data):
        item = ItemModel(**item_data) # this will turn the dicctionary JSON into a keyword argument and we will pass it to ItemModel
        try:
            db.session.add(item) # with this you can add many thing to the database and only commit once, if something was added that shouldn't you can do a rollback of the added
            db.session.commit()
        except SQLAlchemyError:
            abort(500, message = 'An error occurred while inserting the item' )
            
        #check if the item already exist
        ''' for item in items.values():    # we do not need this anymore we are working now with the models in the database, is doing the checking for us
            if(item['name']== item_data["name"] and item['store_id'] == item_data['store_id'] ):
            abort (400, message = f"Item already exist")
                
        item_id = uuid.uuid4().hex
        item = {**item_data, 'id': item_id}
        items[item_id]= item'''

        return item
        