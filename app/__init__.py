from flask import Flask
from app.extensions import db
from app.api.auth import auth_bp
from app.api.tasks import tasks_bp, tasks_api_bp


def create_app(config_class='config.DevelopmentConfig'):
    app = Flask(__name__)
    app.config.from_object(config_class)

    # Inicializa extensiones
    db.init_app(app)

    # Registra blueprints
    app.register_blueprint(auth_bp, url_prefix='/auth')  # Rutas de autenticación
    app.register_blueprint(tasks_bp, url_prefix='/tasks')  # Rutas normales de tareas
    app.register_blueprint(tasks_api_bp)  # Rutas API de tareas

    return app
