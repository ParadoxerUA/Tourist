from marshmallow import Schema, fields, validate, validates_schema, ValidationError
import re


class ChangePasswordSchema(Schema):
    old_password = fields.String()
    new_password = fields.String(required=True)

    @validates_schema
    def _validate_new_password(self, data, **kwargs):
        """password should have at least 8 symbols which has 1 digit and letter"""
        pattern = re.compile(r"^(?=.*[A-Za-z])(?=.*\d)[A-Za-z\d]{8,}$")
        if pattern.match(data['new_password']) is None:
            raise ValidationError("Password should be at least 8 symbols long and have at least one digit and character")
