from marshmallow import Schema, fields, validate


class EquipmentSchema(Schema):
    name = fields.Str(validate=validate.Length(min=3, max=20), required=True)
    weight = fields.Float(required=True, validate=validate.Range(min=0))
    quantity = fields.Integer(required=True, validate=validate.Range(min=1))
    trip_id = fields.Integer(required=True, validate=validate.Range(min=1))
    owner_id = fields.Integer(required=False, validate=validate.Range(min=1))
    role_id = fields.Integer(validate=validate.Range(min=1))

class PatchEquipmentSchema(Schema):
    name = fields.Str(validate=validate.Length(min=3, max=20), required=False)
    weight = fields.Float(required=False, validate=validate.Range(min=0))
    quantity = fields.Integer(required=False, validate=validate.Range(min=1))
    trip_id = fields.Integer(required=False, validate=validate.Range(min=1))
    owner_id = fields.Integer(required=False, validate=validate.Range(min=1))
    role_id = fields.Integer(validate=validate.Range(min=1), required=False)
    amount = fields.Integer(validate=validate.Range(min=1), required=False)
    user_id = fields.Integer(required=False, validate=validate.Range(min=1))
