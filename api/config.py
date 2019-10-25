

class DebugConfig:
    ENV = 'development'
    DEBUG = True
    SQLALCHEMY_DATABASE_URI = 'postgresql://postgres:password@localhost:5432/trip_db'
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    APPS = [
        'smoke_app',
        'user_app',
        'trip_app',
        'role_app',
    ]
    CELERY_APP_NAME = 'tasks'
    CELERY_BROKER_URL = 'redis://localhost:6379/0'


class ProductionConfig:
    ENV = 'development'
    DEBUG = True
    SQLALCHEMY_DATABASE_URI = 'postgresql://postgres:password@localhost:5432/trip_db'
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    APPS = [
        'api.smoke_app',
        'api.user_app',
        'api.trip_app',
        'api.role_app',
    ]
    CELERY_APP_NAME = 'tasks'
    CELERY_BROKER_URL = 'redis://localhost:6379/0'
