from flask import Flask
from app.models import db
from app.routes import register_routes
from config.config import config
from flask_jwt_extended import JWTManager
import os

def create_app(config_name='default'):
    app = Flask(__name__)

    app.config.from_object(config[config_name])

    database_url = os.environ.get('DATABASE_URL', 'sqlite:///talent.db')  # Fallback para SQLite
    app.config['SQLALCHEMY_DATABASE_URI'] = database_url.replace("postgres://", "postgresql://", 1)

    db.init_app(app)

    register_routes(app)

    with app.app_context():
        db.create_all()

    return app

app = create_app()
jwt = JWTManager(app)

if __name__ == '__main__':
    app.run(debug=True, port=5000)