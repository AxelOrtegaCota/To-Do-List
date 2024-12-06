from werkzeug.security import generate_password_hash, check_password_hash

def test_generate_password_hash():
    """Prueba que las contraseñas se hasheen correctamente."""
    password = "securepassword"
    hashed_password = generate_password_hash(password)
    assert hashed_password != password  # El hash no debe ser igual al texto plano
    assert check_password_hash(hashed_password, password)  # El hash debe ser válido para la contraseña

def test_check_password_hash():
    """Prueba que la función check_password_hash valide correctamente."""
    password = "mypassword"
    hashed_password = generate_password_hash(password)
    assert check_password_hash(hashed_password, password)  # Contraseña correcta
    assert not check_password_hash(hashed_password, "wrongpassword")  # Contraseña incorrecta
