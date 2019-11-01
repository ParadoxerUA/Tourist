from config import DebugConfig
from app import create_app

app = create_app(DebugConfig)

def create_users(count):
    for i in range(count):
        user = app.models.User.create_user(name=f'username-{i}', email=f'email-{i}@mail.com',
            password='password321',surname=f'surname-{i}')
        user.activate_user()


create_users(5)