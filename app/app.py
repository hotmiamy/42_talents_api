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

def create_app(config_name='default'):
    app = Flask(__name__)
    app.config.from_object(config[config_name])

    if app.config['SQLALCHEMY_DATABASE_URI'].startswith("postgres://"):
        app.config['SQLALCHEMY_DATABASE_URI'] = app.config['SQLALCHEMY_DATABASE_URI'].replace(
            "postgres://", "postgresql://", 1
        )

    db.init_app(app)
    jwt = JWTManager(app)
    ma = Marshmallow(app)

    register_routes(app)

    with app.app_context():
        max_retries = 5
        for attemp in range(max_retries):
            try:
                if db.engine.url.drivername == 'postgresql':
                        with db.engine.begin() as conn:
                                    conn.execute(text("CREATE EXTENSION IF NOT EXISTS pgcrypto"))
                db.create_all()
                break
            except OperationalError as e:
                if attemp == max_retries - 1:
                    app.logger.error(f"Database conection failed retriging...: ({attemp+1}/{max_retries})")
                    time.sleep(2 * (attempt + 1))
                else:
                    app.logger.error("Failed to connect to database after multiple attempts")
                    raise

    return app

app = create_app()
jwt = JWTManager(app)

if __name__ == '__main__':
    app.run(debug=True, port=5000)