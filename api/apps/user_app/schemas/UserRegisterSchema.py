from marshmallow import Schema, fields, ValidationError, validates
import re


class UserRegisterSchema(Schema):

    name = fields.Str(required=True, error_messages={"required": "Name is required."})
    surname = fields.Str()
    email = fields.Email(required=True, error_messages={"required": "Email is required."})
    password = fields.Str(required=True, error_messages={"required": "Password is required."})

    @validates("password")
    def validate_password_length(self, password):
        """password should have at least 8 symbols which has 1 digit and letter"""
        pattern = re.compile(r"^(?=.*[A-Za-z])(?=.*\d)[A-Za-z\d]{8,}$")
        if pattern.match(password) is None:
            raise ValidationError("Password should be at least 8 symbols long and have at least one digit and character")


    @validates("name")
    def validate_name_length(self, value):
        if len(value) < 2:
            raise ValidationError("Name is to short")
        elif len(value) > 30:
            raise ValidationError("Name is too long")

    @validates("surname")
    def validate_surname_length(self, value):
        if value:
            if len(value) < 2:
                raise ValidationError("Surname is to short")
            elif len(value) > 30:
                raise ValidationError("Surname is too long")




