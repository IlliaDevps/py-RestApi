from db import db

class StoreModel(db.Model): # this become a mapping betwen a row in a table to a python class or pytho objects
    __tablename__ = 'stores'

    id = db.Column(db.Integer, primary_key= True)
    name = db.Column(db.String(80), unique=True , nullable =False)
    items = db.relationship('ItemModel', back_populates= 'store' , lazy='dynamic', cascade= 'all, delete')
