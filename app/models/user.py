from app.extensions import db
from werkzeug.security import generate_password_hash, check_password_hash


class User(db.Model):
    __tablename__ = 'users'

    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=True)
    _password = db.Column("password", db.String(128), nullable=False)  # Campo privado para almacenar la contraseña
    oauth_id = db.Column(db.String(100))  # ID del proveedor OAuth

    # Relación con las tareas
    tasks = db.relationship("Task", backref="user", cascade="all, delete-orphan", lazy=True)

    @property
    def password(self):
        """Evita que la contraseña sea leída directamente."""
        raise AttributeError("Password is not a readable attribute.")

    @password.setter
    def password(self, plaintext_password):
        """Hashea y establece la contraseña."""
        if not plaintext_password:
            raise ValueError("La contraseña no puede estar vacía.")
        self._password = generate_password_hash(plaintext_password)


    def check_password(self, plaintext_password):
        """Verifica si una contraseña sin hashear coincide con la hasheada."""
        if not plaintext_password:
            return False
        return check_password_hash(self._password, plaintext_password)
