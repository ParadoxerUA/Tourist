from database import db
from werkzeug.security import generate_password_hash, check_password_hash


class ValidationError(Exception):
    def __init__(self, *args, **kwargs):
        Exception.__init__(self, *args, **kwargs)


class User(db.Model):
    """Model for user accounts."""

    __tablename__ = 'user_profile'
    __table_args__ = {'extend_existing': True}

    user_id = db.Column(db.Integer, primary_key=True, unique=True)
    name = db.Column(db.String(15), nullable=False)
    surname = db.Column(db.String(60), nullable=True)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password_hash = db.Column(db.String(100), nullable=False)
    avatar = db.Column(db.LargeBinary)
    capacity = db.Column(db.Integer, nullable=False, default=20)
    uuid = db.Column(db.String(36), nullable=True)
    is_active = db.Column(db.Boolean, default=False)
    trips = db.relationship('api.apps.trip_app.models.Trip')

    def __repr__(self):
        return f'<User {self.name}>'

    @classmethod
    def create_user(cls, name, email, password, surname=None):
        password_hash = cls.set_password(password)
        user = cls(name=name, email=email, password_hash=password_hash, surname=surname)
        db.session.add(user)
        db.session.commit()
        return user

    # @classmethod
    # def get_user_by_email(cls, email):
    #     user = cls.query.filter_by(email=email).first()
    #     if user is None:
    #         raise ValidationError(f'There is no user with email={email}')
    #     else:
    #         return user
    #
    # @classmethod
    # def get_user_by_id(cls, id):
    #     user = cls.query.filter_by(user_id=id).first()
    #     if user is None:
    #         raise ValidationError(f'There is no user with id={id}')
    #     else:
    #         return user
    #
    # @classmethod
    # def get_by_uuid(cls, uuid):
    #     user = cls.query.filter_by(uuid).first()
    #     if user is None:
    #         raise ValidationError(f'There is no user with uuid={uuid}')
    #     else:
    #         return user

    @classmethod
    def get_user(cls, **search_params):
        '''returns user that matches data in search params'''

        return User.query.filter_by(**search_params).first()

    @classmethod
    def set_password(cls, password):
        return generate_password_hash(password)

    @classmethod
    def check_password(cls, password):
        return check_password_hash(generate_password_hash(password), password)

    def activate_user(self):
        self.is_active = True
        db.session.add(self)
        db.session.commit()

    def change_capacity(self, capacity):
        self.capacity = capacity
        db.session.add(self)
        db.session.commit()

    @classmethod
    def user_exists(cls, **search_params):
        return bool(cls.query.filter_by(**search_params).first())
