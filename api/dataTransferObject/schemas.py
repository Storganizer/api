from flasgger import Schema, fields


class LocationSchema(Schema):

    id = fields.Int(required=True)
    name = fields.Str(required=True)
    description = fields.Str()
    image = fields.Str()
    classification = fields.Int()
    #boxes = fields.Nested(BoxSchema, many=True)
    #"uri": fields.Url('todo_resource')
