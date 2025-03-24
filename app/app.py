from flask import Flask
from app.models import db
from app.routes import register_routes
from config.config import config
from flask_jwt_extended import JWTManager
import os
from flask_marshmallow import Marshmallow
from sqlalchemy import text 
from sqlalchemy.exc import OperationalError
import time
from flask_migrate import Migrate

def create_app(config_name='default'):
    app = Flask(__name__)
    app.config.from_object(config[config_name])

    if app.config['SQLALCHEMY_DATABASE_URI'].startswith("postgres://"):
        app.config['SQLALCHEMY_DATABASE_URI'] = app.config['SQLALCHEMY_DATABASE_URI'].replace(
            "postgres://", "postgresql://", 1
        )

    db.init_app(app)

    register_routes(app)
    migrate = Migrate(app, db)
    return app

app = create_app()
jwt = JWTManager(app)

if __name__ == '__main__':
    app.run(debug=True, port=5000)