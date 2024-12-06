from flask import Flask
from app.extensions import db
from app.api.auth import auth_bp

def create_app(config_class='config.Config'):
    app = Flask(__name__)
    app.config.from_object(config_class)

    # Inicializa extensiones
    db.init_app(app)

    # Registra blueprints
    app.register_blueprint(auth_bp, url_prefix='/auth')

    return app
