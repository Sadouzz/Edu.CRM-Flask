import os
from dotenv import load_dotenv

load_dotenv()
class Config:
    APP_NAME = os.getenv('APP_NAME', 'MyFlaskApp')
    FLASK_ENV = os.getenv('FLASK_ENV', 'development')
    FLASK_DEBUG = os.getenv('FLASK_DEBUG', 'True') == 'True'
    FLASK_APP = os.getenv('FLASK_APP', 'app.py')
    SECRET_KEY = os.getenv('SECRET_KEY', '')
    DEBUG = FLASK_DEBUG

    SQLALCHEMY_DATABASE_URI = os.getenv('DATABASE_URL')

    if SQLALCHEMY_DATABASE_URI and SQLALCHEMY_DATABASE_URI.startswith("postgres://"):
        SQLALCHEMY_DATABASE_URI = SQLALCHEMY_DATABASE_URI.replace("postgres://", "postgresql://", 1)
        
    SQLALCHEMY_TRACK_MODIFICATIONS = False
config = Config()