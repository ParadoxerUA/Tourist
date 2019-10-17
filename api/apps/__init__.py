from .smoke_app import app as smoke_app
from .trip_app import app as trip_app
from .user_app import app as user_app

APPS = [
    smoke_app,
    user_app,
    trip_app,
]
