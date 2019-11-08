from marshmallow import Schema, fields, validate


class EqSchema(Schema):
    name = fields.Str(validate=validate.Length(min=3, max=20), required=True)
    weight = fields.Integer(required=True, validate=validate.Range(min=0))
    quantity = fields.Integer(required=True, validate=validate.Range(min=1))
    trip_id = fields.Integer(required=True, validate=validate.Range(min=1))
