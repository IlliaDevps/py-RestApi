import uuid
from flask import request
from flask.views import MethodView
from flask_smorest import Blueprint, abort
from sqlalchemy.exc import SQLAlchemyError, IntegrityError


from db import db
from  models import StoreModel
from schemas import StoreSchema

blp = Blueprint('stores', __name__, description = 'Operation on Stores')

@blp.route('/store/<string:store_id>')
class Store(MethodView):
    @blp.response(200,  StoreSchema)
    def get(self, store_id):
            store = StoreModel.query.get_or_404(store_id)
            return store           
           
            '''try:
                return stores[store_id],201
            except KeyError:
                    abort(404, message= 'Store not found')'''
    
    def delete(self, store_id):
            store = StoreModel.query.get_or_404(store_id)
            raise NotImplementedError("Deleting a store is not implemented")
            '''try:
                del stores[store_id]
                return {"message": "Store deleted"}
            except KeyError:
                abort(404, message= 'Store not found')'''

@blp.route('/store')
class StoreList(MethodView):
     @blp.response(200,  StoreSchema(many=True))
     def get(self):
          return stores.values()
     @blp.arguments(StoreSchema)
     @blp.response(201,  StoreSchema)
     def post(self, store_data):
            store = StoreModel(**store_data)
            try:
                 db.session.add(store)
                 db.session.commit()
            except IntegrityError:
                 abort(400, message = 'A store with that name already exists')
            except SQLAlchemyError:
                 abort(500, message= 'An error occurred creating the store')
            ''' for store in stores.values():
                    if(store_data['name']==store['name']):
                           abort (400, message = "Store already exist")
                store_id = uuid.uuid4().hex
                store = {**store_data, 'id': store_id}
                stores[store_id]=  store #not more a list is a dictionary stores.append(new_store)'''  # no longer need this we are working now with the models in the database, is doing the checking for us
            return store
     