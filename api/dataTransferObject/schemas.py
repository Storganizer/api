from flask_restful import fields

Location = {
    "id": fields.Integer(),
    "name": fields.String(),
    "description": fields.String(),
    "image": fields.String(),
    "classification": fields.Integer()#,
    #"uri": fields.Url('todo_resource')
}