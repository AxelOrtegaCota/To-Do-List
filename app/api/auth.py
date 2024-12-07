from flask import Blueprint, request, render_template, redirect, url_for, session
from app.models.user import User
from app.extensions import db

auth_bp = Blueprint('auth', __name__)

@auth_bp.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'GET':
        # Renderizar el formulario de login
        return render_template('auth/login.html')

    # Manejo de solicitudes POST
    username = request.form.get('username')
    password = request.form.get('password')

    if not username or not password:
        return render_template('auth/login.html', error='Se requiere usuario y contraseña')

    # Verificar usuario en la base de datos
    user = User.query.filter_by(username=username).first()
    if user and user.check_password(password):
        session['user_id'] = user.id
        session['username'] = user.username
        return redirect(url_for('tasks.todo_list'))  # Redirigir a las tareas

    return render_template('auth/login.html', error='Usuario o contraseña incorrectos')

@auth_bp.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'GET':
        # Renderizar el formulario de registro
        return render_template('auth/register.html')

    # Manejo de solicitudes POST para registro
    username = request.form.get('username')
    password = request.form.get('password')

    if not username or not password:
        return render_template('auth/register.html', error='Se requiere usuario y contraseña')

    # Verificar si el usuario ya existe
    user = User.query.filter_by(username=username).first()
    if user:
        return render_template('auth/register.html', error='El usuario ya existe')

    # Crear un nuevo usuario
    new_user = User(username=username)
    new_user.password = password  # Esto debe manejarse con hashing seguro
    db.session.add(new_user)
    db.session.commit()

    return redirect(url_for('auth.login'))
