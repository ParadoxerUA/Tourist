from marshmallow import Schema, fields, pprint

class TripSchema(Schema):
    name = fields.Str()
    description = fields.Str()
    start_date = fields.Date()
    end_date = fields.Date()
    status = fields.Bool()