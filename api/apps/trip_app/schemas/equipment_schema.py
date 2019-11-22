from marshmallow import Schema, fields, validate


class EquipmentSchema(Schema):
    name = fields.Str(validate=validate.Length(min=3, max=20), required=True)
    weight = fields.Float(required=True, validate=validate.Range(min=0))
    quantity = fields.Integer(required=True, validate=validate.Range(min=1))
