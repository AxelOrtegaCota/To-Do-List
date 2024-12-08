import os

class Config:
    """Configuración base."""
    SECRET_KEY = os.getenv('SECRET_KEY', 'default_secret_key')
    SQLALCHEMY_TRACK_MODIFICATIONS = False

class DevelopmentConfig(Config):
    """Configuración para desarrollo."""
    DEBUG = True
    SQLALCHEMY_DATABASE_URI = 'sqlite:///development.db'  # Usar SQLite para desarrollo

class TestingConfig(Config):
    """Configuración específica para pruebas."""
    TESTING = True
    SQLALCHEMY_DATABASE_URI = 'sqlite:///:memory:'  # Usa una base de datos en memoria para pruebas
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    SECRET_KEY = 'testing-secret'
    SERVER_NAME = 'localhost'  # Necesario para usar `url_for` en las pruebas
    WTF_CSRF_ENABLED = False

class ProductionConfig(Config):
    """Configuración para producción."""
    SQLALCHEMY_DATABASE_URI = os.getenv('DATABASE_URL', 'sqlite:///production.db')
