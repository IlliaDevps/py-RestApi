from marshmallow import Schema,fields

# we use marshmallow for validation


class PlainItemSchema(Schema):
    id = fields.Int(dump_only=True)
    name= fields.Str(required = True)
    price= fields.Float(required = True)

class PlainStoreSchema(Schema):
    id = fields.Int(dump_only=True)
    name = fields.Str(required=True)  

class PlainTagSchema(Schema):
    id = fields.Int(dump_only=True)
    name = fields.Str(required=True)  

class ItemUpdateSchema(Schema):
    name = fields.Str()
    price= fields.Float()
    store_id = fields.Int()

class ItemSchema(PlainItemSchema):
    store_id = fields.Int(required=True, load_only=True) # the opposite of dump_only = True
    store = fields.Nested(PlainStoreSchema(), dump_only = True) #  dump_only = True  means we use this one when retrun data to the client not when receiving

class StoreSchema(PlainStoreSchema):
    items= fields.List(fields.Nested(PlainItemSchema()), dump_only = True)
    tags= fields.List(fields.Nested(PlainTagSchema()), dump_only = True)

class TagSchema(PlainTagSchema):
    store_id = fields.Int( load_only=True)
    store = fields.Nested(PlainStoreSchema(), dump_only = True)