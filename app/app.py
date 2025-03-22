from flask import Flask
from models import db
from routes import register_routes
from config import config
from flask_jwt_extended import JWTManager

def create_app(config_name='default'):
    app = Flask(__name__)
    app.config.from_object(config[config_name])

    db.init_app(app)

    register_routes(app)

    with app.app_context():
        db.create_all()

    return app

app = create_app()
jwt = JWTManager(app)

if __name__ == '__main__':
    app.run(debug=True, port=5000)