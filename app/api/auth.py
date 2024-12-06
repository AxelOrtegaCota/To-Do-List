from flask import Blueprint, request, jsonify, session
from werkzeug.security import generate_password_hash, check_password_hash
from app.models.user import User
from app.extensions import db

# Crear el Blueprint para las rutas de autenticación
auth_bp = Blueprint('auth', __name__)

@auth_bp.route('/login', methods=['POST'])
def login():
    """Endpoint para iniciar sesión."""
    data = request.get_json()
    username = data.get('username')
    password = data.get('password')

    if not username or not password:
        return jsonify({'error': 'Se requiere usuario y contraseña'}), 400

    user = User.query.filter_by(username=username).first()
    if user and user.check_password(password):
        # Crear sesión del usuario
        session['user_id'] = user.id
        session['username'] = user.username
        return jsonify({'message': f'Bienvenido {user.username}'}), 200

    return jsonify({'error': 'Usuario o contraseña incorrectos'}), 401

@auth_bp.route('/register', methods=['POST'])
def register():
    """Endpoint para registrar un nuevo usuario."""
    data = request.get_json()
    username = data.get('username')
    password = data.get('password')

    if not username or not password:
        return jsonify({'error': 'Se requiere usuario y contraseña'}), 400

    if User.query.filter_by(username=username).first():
        return jsonify({'error': 'El usuario ya existe'}), 400

    new_user = User(username=username)
    new_user.password = password

    db.session.add(new_user)
    db.session.commit()

    return jsonify({'message': f'Usuario {username} registrado exitosamente'}), 201

@auth_bp.route('/logout', methods=['POST'])
def logout():
    """Endpoint para cerrar sesión."""
    session.clear()
    return jsonify({'message': 'Sesión cerrada correctamente'}), 200
