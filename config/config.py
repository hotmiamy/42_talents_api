import os
from dotenv import load_dotenv

load_dotenv()

class Config:
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    SECRET_KEY = os.getenv('FLASK_SECRET_KEY')
    JWT_SECRET_KEY = os.getenv('JWT_SECRET_KEY')   
    JWT_TOKEN_LOCATION = ['headers']
    UPLOAD_FOLDER = os.getenv('UPLOAD_FOLDER')
    MAX_CV_SIZE = 5 * 1024 * 1024

class DevelopmentConfig(Config):
    SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL', 'sqlite:///talent.db')
    DEBUG = True
    JWT_ACCESS_TOKEN_EXPIRES = False

class ProductionConfig(Config):
    SQLALCHEMY_DATABASE_URI = (
        os.environ.get('DATABASE_URL', '')
        .replace("postgres://", "postgresql://", 1))
    DEBUG = False
    JWT_ACCESS_TOKEN_EXPIRES = 3600

class TestingConfig(Config):
    TESTING = True
    SQLALCHEMY_DATABASE_URI = "sqlite:///:memory:"
    DEBUG = True

config = {
    'development': DevelopmentConfig,
    'production': ProductionConfig,
    'testing': TestingConfig,
    'default': DevelopmentConfig
}