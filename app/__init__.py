import os
from flask import Flask, redirect, url_for
from app.extensions import db, migrate, oauth
from app.api.auth import auth_bp
from app.api.tasks import tasks_bp, tasks_api_bp
from app.utils.jokes import jokes_bp
from app.api.oauth import oauth_bp
from dotenv import load_dotenv

def create_app(config_class='config.DevelopmentConfig'):
    app = Flask(__name__)
    app.config.from_object(config_class)

    # Inicializa extensiones
    db.init_app(app)
    migrate.init_app(app, db)
    oauth.init_app(app)

    with app.app_context():
        db.create_all()  # Esto asegura que las tablas se crean si no existen.

    oauth.register(
        name='google',
        client_id=os.getenv('GOOGLE_CLIENT_ID'),
        client_secret=os.getenv('GOOGLE_CLIENT_SECRET'),
        access_token_url='https://oauth2.googleapis.com/token',
        authorize_url='https://accounts.google.com/o/oauth2/auth',
        api_base_url='https://www.googleapis.com/oauth2/v1/',
        client_kwargs={
            'scope': 'openid email profile',
        },
    )

    # Define la ruta raíz para redirigir al login
    @app.route("/")
    def root():
        return redirect(url_for("auth.login"))

    # Registra blueprints
    app.register_blueprint(auth_bp, url_prefix='/auth')  # Rutas de autenticación
    app.register_blueprint(tasks_bp, url_prefix='/tasks')  # Rutas normales de tareas
    app.register_blueprint(tasks_api_bp)  # Rutas API de tareas
    app.register_blueprint(jokes_bp, url_prefix="/jokes")  # Rutas relacionadas con chistes
    app.register_blueprint(oauth_bp, url_prefix='/oauth')  # Rutas de OAuth

    return app
