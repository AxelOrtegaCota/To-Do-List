from flask import Blueprint, request, jsonify, session, redirect, url_for, render_template
from app.models.user import User
from app.extensions import db


auth_bp = Blueprint('auth', __name__)


@auth_bp.route('/register', methods=['GET', 'POST'])
def register():
    """Registro de usuario"""
    if request.method == 'GET':
        # Renderiza el formulario HTML de registro
        return render_template('auth/register.html')

    # Manejo de solicitudes POST (formulario o API)
    username = request.form.get('username') or request.json.get('username')
    password = request.form.get('password') or request.json.get('password')

    if not username or not password:
        if request.content_type == 'application/json':
            return jsonify({'error': 'Se requiere usuario y contraseña'}), 400
        return render_template('auth/register.html', error='Se requiere usuario y contraseña')

    if User.query.filter_by(username=username).first():
        if request.content_type == 'application/json':
            return jsonify({'error': 'El usuario ya existe'}), 400
        return render_template('auth/register.html', error='El usuario ya existe')

    # Crear y guardar un nuevo usuario
    new_user = User(username=username)
    new_user.password = password  # Usar el setter
    db.session.add(new_user)
    db.session.commit()

    if request.content_type == 'application/json':
        return jsonify({'message': f'Usuario {username} registrado exitosamente'}), 201
    return redirect(url_for('auth.login'))


@auth_bp.route('/login', methods=['GET', 'POST'])
def login():
    """Inicio de sesión"""
    if request.method == 'GET':
        return render_template('auth/login.html')

    # Manejo de datos JSON o formulario
    if request.is_json:
        data = request.get_json()
        username = data.get('username')
        password = data.get('password')
    else:
        username = request.form.get('username')
        password = request.form.get('password')

    # Validar credenciales
    if not username or not password:
        if request.is_json:
            return jsonify({'error': 'Se requiere usuario y contraseña'}), 400
        return render_template('auth/login.html', error='Se requiere usuario y contraseña')

    user = User.query.filter_by(username=username).first()
    if user and user.check_password(password):
        session['user_id'] = user.id
        session['username'] = user.username
        if request.is_json:
            return jsonify({'message': f'Bienvenido {user.username}'}), 200
        return redirect(url_for('tasks.todo_list'))

    # Respuesta para credenciales inválidas
    if request.is_json:
        return jsonify({'error': 'Credenciales inválidas'}), 401  # Devuelve 401 para API JSON
    return render_template('auth/login.html', error='Credenciales inválidas')


@auth_bp.route('/logout', methods=['GET', 'POST'])
def logout():
    """Cierre de sesión"""
    session.clear()
    if request.method == 'POST':
        return jsonify({'message': 'Sesión cerrada correctamente'}), 200
    # Redirección para solicitudes GET (usualmente desde un navegador)
    return redirect(url_for('auth.login'))
