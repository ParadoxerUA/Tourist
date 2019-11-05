from database import db
from werkzeug.security import generate_password_hash, check_password_hash
from datetime import datetime


class User(db.Model):
    """Model for user accounts."""

    __tablename__ = 'user_profile'
    __table_args__ = {'extend_existing': True}

    user_id = db.Column(db.Integer, primary_key=True, unique=True)
    name = db.Column(db.String(15), nullable=False)
    surname = db.Column(db.String(60), nullable=True)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password_hash = db.Column(db.String(100), nullable=False)
    avatar = db.Column(db.String(250), nullable=True)
    capacity = db.Column(db.Integer, nullable=False, default=20)
    uuid = db.Column(db.String(36), nullable=True)
    is_active = db.Column(db.Boolean, default=False)
    registration_time = db.Column(db.DateTime, default=datetime.utcnow())

    def __repr__(self):
        return f'<User {self.name}>'

    @classmethod
    def create_user(cls, name, email, password, surname=None):
        password_hash = cls.set_password(password)
        user = cls(name=name, email=email, password_hash=password_hash, surname=surname, )
        db.session.add(user)
        db.session.commit()
        return user

    def set_uuid(self, uuid):
        self.uuid = uuid
        db.session.add(self)
        db.session.commit()

    def delete_user(self):
        db.session.delete(self)
        db.session.commit()


    @classmethod
    def get_user_by_id(cls, user_id):
        return cls.query.filter_by(user_id=user_id).first()

    @classmethod
    def get_user_by_email(cls, email):
        return cls.query.filter_by(email=email).first()

    @classmethod
    def get_user_by_uuid(cls, uuid):
        return User.query.filter_by(uuid=uuid).first()

    @classmethod
    def set_password(cls, password):
        return generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)

    def activate_user(self):
        self.is_active = True
        db.session.add(self)
        db.session.commit()

    def change_capacity(self, capacity):
        self.capacity = capacity
        db.session.add(self)
        db.session.commit()

    def is_uuid_valid(self):
        datetime_diff = datetime.utcnow() - self.registration_time
        diff_in_hours = datetime_diff.total_seconds() / 3600
        if diff_in_hours > 24:
            return False
        return True

    def  get_public_data(self):
        public_data = {
            "avatar": self.avatar,
            "capacity": self.capacity,
            "name": self.name,
            "surname": self.surname,
            "user_id": self.user_id,
        }
        return public_data