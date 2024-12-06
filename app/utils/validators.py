from werkzeug.security import check_password_hash
from app.models.user import User

def validate_login_form(data):
    """
    Valida el formulario de inicio de sesión.

    :param data: Diccionario con los datos del formulario (usuario, contraseña)
    :return: True si la validación es exitosa, False si hay algún error.
    """
    username = data.get('username')
    password = data.get('password')

    if not username or not password:
        return False

    # Verificar que el usuario exista y la contraseña sea correcta
    user = User.query.filter_by(username=username).first()
    if user and check_password_hash(user.password, password):
        return True
    return False

def validate_register_form(data):
    """
    Valida el formulario de registro.

    :param data: Diccionario con los datos del formulario (usuario, contraseña, confirmación de contraseña)
    :return: True si la validación es exitosa, False si hay algún error.
    """
    username = data.get('username')
    password = data.get('password')
    confirm_password = data.get('confirm_password')

    if not username or not password or not confirm_password:
        return False

    # Verificar que las contraseñas coincidan
    if password != confirm_password:
        return False

    # Verificar que el nombre de usuario no exista ya
    existing_user = User.query.filter_by(username=username).first()
    if existing_user:
        return False

    return True
