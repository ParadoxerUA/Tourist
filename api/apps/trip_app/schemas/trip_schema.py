from marshmallow import Schema, fields, validates_schema, ValidationError
import datetime


class TripSchema(Schema):
    name = fields.Str()
    description = fields.Str()
    start_date = fields.Date()
    end_date = fields.Date()
    status = fields.Bool()

    @validates_schema
    def validate_date(self, data, **kwargs):
        start_date = data['start_date']
        end_date = data['end_date']
        if start_date > end_date:
            raise ValidationError("Start date can not be greater than end date")
        else:
            print("HELLO\n"*20)
