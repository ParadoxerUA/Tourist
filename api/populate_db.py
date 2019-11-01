from config import DebugConfig
from app import create_app

app = create_app(DebugConfig)

def create_users(from_number, amount):
    for i in range(from_number, from_number + amount):
        user = app.models.User.create_user(name=f'username-{i}', email=f'email-{i}@mail.com',
            password='password321',surname=f'surname-{i}')
        user.activate_user()

# to create 5 new users
# create_users(0, 5)

# Some stuff for interactive using of sqlalchemy
db = app.db
User = app.models.User
Trip = app.models.Trip

user = User.query.first()
trip = Trip.query.first()

