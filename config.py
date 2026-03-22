import os

class Config:
    # =========================
    # CONFIG APP
    # =========================
    APP_NAME = os.getenv('APP_NAME', 'MyFlaskApp')
    FLASK_ENV = os.getenv('FLASK_ENV', 'development')
    DEBUG = os.getenv('FLASK_DEBUG', 'True') == 'True'
    SECRET_KEY = os.getenv('SECRET_KEY', 'super-secret-key')

    # =========================
    # DATABASE CONFIG
    # =========================
    DATABASE_URL = os.getenv('DATABASE_URL')

    # fallback si DATABASE_URL non défini
    if DATABASE_URL:
        SQLALCHEMY_DATABASE_URI = DATABASE_URL
    else:
        SQLALCHEMY_DATABASE_URI = "postgresql://postgres:fadil2006@localhost:5432/school_db"

    # correction compatibilité Heroku / Render
    if SQLALCHEMY_DATABASE_URI.startswith("postgres://"):
        SQLALCHEMY_DATABASE_URI = SQLALCHEMY_DATABASE_URI.replace(
            "postgres://", "postgresql://", 1
        )

    SQLALCHEMY_TRACK_MODIFICATIONS = False

    # =========================
    # OPTIONS BONUS (PRO)
    # =========================
    SQLALCHEMY_ENGINE_OPTIONS = {
        "pool_pre_ping": True,  # évite les connexions mortes
        "pool_recycle": 300
    }


config = Config()