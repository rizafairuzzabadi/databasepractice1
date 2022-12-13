from marshmallow import Schema, fields


class ItemSchema(Schema):
    id = fields.Str(dump_only=True) # dump_only=True means that this field will not be required when creating a new item
    name = fields.Str(required=True) # required=True means that this field is required when creating a new item
    price = fields.Float(required=True) # required=True means that this field is required when creating a new item
    store_id = fields.Str(required=True) # required=True means that this field is required when creating a new item

class ItemUpdateSchema(Schema):
    name = fields.Str()
    price = fields.Float()

class StoreSchema(Schema):
    id = fields.Str(dump_only=True) # dump_only=True means that this field will not be required when creating a new store
    name = fields.Str(required=True) # required=True means that this field is required when creating a new store