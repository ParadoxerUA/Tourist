from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()


def set_db(main_app):
    # import your models below
    from apps.role_app.models import Role
    from apps.user_app.models import User

    db.init_app(main_app)
    db.create_all()

