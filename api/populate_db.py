from config import DebugConfig
from app import create_app

app = create_app(DebugConfig)
db = app.db

User = app.models.User
Trip = app.models.Trip

users = User.query.all()
trips = Trip.query.all()

def create_users(from_number, amount):
    '''to create 2 new users:\n
    create_users(0, 2)\n
    function doesnt check for right naming, 
    therefore beware to choose right <from_number>'''
    created_users = []
    for i in range(from_number, from_number + amount):
        user = User.create_user(name=f'username-{i}', email=f'email-{i}@mail.com',
            password='password321',surname=f'surname-{i}')
        user.activate_user()
        created_users.append(user)
    return created_users

# def create_trips(from_number, amount, admin=None):
#     created_trips = []
#     for i in range(from_number, from_number + amount):
#         trip = Trip.create_trip(
#             name="name",
#             description="desc",
#             start_date="2014-12-22T03:12:58.019077+00:00",
#             end_date="2015-12-22T03:12:58.019077+00:00",
#         )


# to create 5 new users
create_users(0, 5)

# user = User.query.first()
# trip = Trip.query.first()

