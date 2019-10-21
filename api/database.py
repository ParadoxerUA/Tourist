from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()


def set_db(main_app):
    # import your models below
    from apps.trip_app.models import Trip
    db.init_app(main_app)
