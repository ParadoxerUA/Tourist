class ProductionConfig:
    ENV = 'development'
    DEBUG = True
    SQLALCHEMY_DATABASE_URI = 'postgresql://postgres:password@host.docker.internal:5432/trip_db'
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    APPS = [
        'api.smoke_app',
        'api.user_app',
        'api.trip_app',
        'api.role_app',
        'api.equipment_app',
    ]
    UPLOAD_FOLDER = "/data/images/user_avatar/"
    CELERY_APP_NAME = 'tasks'
    CELERY_BROKER_URL = 'redis://redis:6379/0'
