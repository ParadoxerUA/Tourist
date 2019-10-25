from .smoke_app import app as smoke_app
from .trip_app import app as trip_app
from .user_app import app as user_app
from .role_app import app as role_app
from .otc_app import app as otc_app

APPS = [
    smoke_app,
    user_app,
    trip_app,
    role_app,
    otc_app,
]
