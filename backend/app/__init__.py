from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS
from flask_migrate import Migrate
from .config import Config

db = SQLAlchemy()
migrate = Migrate()

def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)

    CORS(app)

    db.init_app(app)
    migrate.init_app(app, db)

    from .routes import main as main_blueprint
    app.register_blueprint(main_blueprint)

    return app
