from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()


def set_db(main_app):
    # import your models below

    db.init_app(main_app)
