from apps.user_app.models import User, ValidationError


class UserController:

    @classmethod
    def register_user(cls, name, email, password, surname=None):
        try:
            User.get_user(email=email)
        except ValidationError as err:
            User.create_user(name=name, email=email, password=password, surname=surname)
        else:
            return {"error": f"user with this email={email} already exists"}

    @classmethod
    def activate_user(cls, user_id):
        user = User.get_user(user_id=user_id)
        user.activate_user()

    @classmethod
    def change_capacity(cls, user_id, capacity):
        user = User.get_user(user_id=user_id)
        user.change_capacity(capacity)

