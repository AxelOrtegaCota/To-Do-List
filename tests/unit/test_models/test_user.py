from app.models.user import User


def test_user_creation(init_database):
    """Prueba para la creación de usuarios."""
    user = User(username="testuser")
    user.password = "plaintextpassword"  # Utiliza el setter para asignar la contraseña

    assert user.username == "testuser"
    assert user._password != "plaintextpassword"  # Verifica que la contraseña no se almacene como texto plano
    assert user.check_password("plaintextpassword")  # Verifica que la contraseña sea válida
