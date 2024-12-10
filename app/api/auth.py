from flask import Blueprint, request, jsonify, session, redirect, url_for, render_template
from app.models.user import User
from app.extensions import db

auth_bp = Blueprint('auth', __name__)

@auth_bp.route('/register', methods=['GET', 'POST'])
def register():
    """User registration"""
    if request.method == 'GET':
        return render_template('auth/register.html')

    # Manejo de solicitudes POST
    if request.is_json:
        data = request.get_json()
        username = data.get('username')
        email = data.get('email')
        password = data.get('password')
    else:
        username = request.form.get('username')
        email = request.form.get('email')
        password = request.form.get('password')

    # Validaciones
    if not username or not email or not password:
        error_message = 'Username, email, and password are required'
        if request.is_json:
            return jsonify({'error': error_message}), 400
        return render_template('auth/register.html', error=error_message)

    # Verifica si el email ya existe
    existing_user = User.query.filter_by(email=email).first()
    if existing_user:
        error_message = 'Email is already in use'
        if request.is_json:
            return jsonify({'error': error_message}), 400
        return render_template('auth/register.html', error=error_message)

    # Crear el usuario y guardar en la base de datos
    try:
        new_user = User(username=username, email=email)
        new_user.password = password  # Usar el setter para el hashing
        db.session.add(new_user)
        db.session.commit()
        print(f"User {username} successfully registered")  # Debugging
    except Exception as e:
        print(f"Error saving user to database: {e}")  # Debugging
        db.session.rollback()
        error_message = 'An error occurred while saving the user'
        if request.is_json:
            return jsonify({'error': error_message}), 500
        return render_template('auth/register.html', error=error_message)

    # Respuesta según el tipo de solicitud
    if request.is_json:
        return jsonify({'message': f'User {username} successfully registered'}), 201

    # Redirige al login en caso de solicitud HTML
    return redirect(url_for('auth.login')), 302


@auth_bp.route('/login', methods=['GET', 'POST'])
def login():
    """User login"""
    if request.method == 'GET':
        return render_template('auth/login.html')

    # Handle JSON or form data
    if request.is_json:
        data = request.get_json()
        username = data.get('username')
        password = data.get('password')
    else:
        username = request.form.get('username')
        password = request.form.get('password')

    # Validate credentials
    if not username or not password:
        error_message = 'Username and password are required'
        if request.is_json:
            return jsonify({'error': error_message}), 400
        return render_template('auth/login.html', error=error_message)

    user = User.query.filter_by(username=username).first()
    if user and user.check_password(password):
        session['user_id'] = user.id
        session['username'] = user.username
        if request.is_json:
            return jsonify({'message': f'Welcome {user.username}'}), 200
        return redirect(url_for('tasks.todo_list'))

    # Response for invalid credentials
    error_message = 'Invalid credentials'
    if request.is_json:
        return jsonify({'error': error_message}), 401
    return render_template('auth/login.html', error=error_message), 401


@auth_bp.route('/logout', methods=['GET', 'POST'])
def logout():
    """User logout"""
    session.clear()
    if request.method == 'POST':
        return jsonify({'message': 'Successfully logged out'}), 200
    # Redirection for GET requests (usually from a browser)
    return redirect(url_for('auth.login'))
