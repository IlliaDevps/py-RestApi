from db import db

class ItemModel(db.Model): # this become a mapping betwen a row in a table to a python class or pytho objects
    __tablename__ = 'items'
    id = db.Column(db.Integer, primary_key= True)
    name = db.Column(db.String(80), unique=True , nullable =False)
    price = db.Column(db.Float(precision=2), unique=True , nullable =False)
    store_id = db.Column(db.Integer, unique=True , nullable =False )