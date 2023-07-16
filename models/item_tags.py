from db import db
# this table crete a many to many relation in our SQL database betwen items and tags
class ItemTags(db.Model):
    __tablename__ = 'items_tags'

    id = db.Column(db.Integer, primary_key = True)
    item_id = db.Column(db.Integer, db.ForeignKey('items.id') )
    tag_id = db.Column(db.Integer, db.ForeignKey('tags.id')  )