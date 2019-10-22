from marshmallow import Schema, fields, validates_schema, ValidationError, validate


class TripSchema(Schema):
    name = fields.Str(validate=validate.Length(min=3, max=20))
    description = fields.Str(validate=validate.Length(max=200))
    start_date = fields.Date()
    end_date = fields.Date()
    status = fields.Bool()

    @validates_schema
    def validate_date(self, data, **kwargs):
        start_date = data['start_date']
        end_date = data['end_date']
        if start_date > end_date:
            raise ValidationError("Start date can not be greater than end date")
