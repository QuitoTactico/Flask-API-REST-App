from marshmallow import Schema, fields

# ============= PLAIN ===============

# ------------- item ----------------


class PlainItemSchema(Schema):
    id = fields.Int(dump_only=True)
    name = fields.Str(required=True)
    price = fields.Float(required=True)
    description = fields.Str()


class ItemUpdateSchema(Schema):
    name = fields.Str()
    price = fields.Float()
    description = fields.Str()
    store_id = fields.Int()


# -------------- store ---------------


class PlainStoreSchema(Schema):
    id = fields.Int(dump_only=True)
    name = fields.Str(required=True)


# --------------- tags ---------------


class PlainTagSchema(Schema):
    id = fields.Int(dump_only=True)
    name = fields.Str()


# --------------- user ---------------


class UserSchema(Schema):
    id = fields.Int(dump_only=True)
    username = fields.Str(required=True)
    password = fields.Str(required=True, load_only=True)


# ========== WITH RELATIONS ==========

# toca así. No puedes usar ItemSchema en StoreSchema ni visceversa, porque el otro no existirá aún
# y podrías hacerle lazy al final, usando lambda: ____Schema, pero habrá una anidación infinita
# así que toca poner la versión Plain, que no tiene referencias a nadie


class ItemSchema(PlainItemSchema):
    # store_id = fields.Str(required=True)
    store_id = fields.Int(required=True, load_only=True)
    store = fields.Nested(PlainStoreSchema(), dump_only=True)
    tags = fields.List(fields.Nested(PlainTagSchema()), dump_only=True)


class StoreSchema(PlainStoreSchema):
    items = fields.List(fields.Nested(PlainItemSchema()), dump_only=True)
    tags = fields.List(fields.Nested(PlainTagSchema()), dump_only=True)


class TagSchema(PlainTagSchema):
    store_id = fields.Int(load_only=True)
    items = fields.List(fields.Nested(PlainItemSchema()), dump_only=True)
    store = fields.Nested(PlainStoreSchema(), dump_only=True)


class TagAndItemSchema(Schema):
    message = fields.Str()
    item = fields.Nested(ItemSchema)
    tag = fields.Nested(TagSchema)
