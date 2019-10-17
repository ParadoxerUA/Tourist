from flask_script import Manager
from flask_migrate import Migrate, MigrateCommand
from database import db
from app import create_app
# import your models below


if __name__ == '__main__':
    from config import DebugConfig
    app = create_app(DebugConfig)
    db.init_app(app)
    migrate = Migrate(app, db)
    manager = Manager(app)
    manager.add_command('db', MigrateCommand)
    manager.run()
