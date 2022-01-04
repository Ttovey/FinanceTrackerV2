from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from financeTracker.config import Config
from flask_migrate import Migrate

db = SQLAlchemy()
migrate = Migrate()


def create_app(config_class=Config):
    app = Flask(__name__)
    app.config.from_object(Config)
    app.config['SECRET_KEY'] = 'a temporary secret key'

    db.init_app(app)
    migrate.init_app(app, db)

    from financeTracker.plaid.routes import bank
    from financeTracker.user.routes import user

    app.register_blueprint(bank)
    app.register_blueprint(user)

    return app
