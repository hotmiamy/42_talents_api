import os

class Config:
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    SECRET_KEY = os.environ.get('SECRET_KEY', 'dev-key')
    JWT_SECRET_KEY = os.environ.get('JWT_SECRET_KEY', 'super-secret')   
    JWT_TOKEN_LOCATION = ['headers']
    UPLOAD_FOLDER = os.environ.get('UPLOAD_FOLDER', 'uploads')
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

config = {
    'development': DevelopmentConfig,
    'production': ProductionConfig,
    'default': DevelopmentConfig
}