from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()


def set_db(main_app):
    # import your models below
    from apps.role_app.models import Role

    db.init_app(main_app)
