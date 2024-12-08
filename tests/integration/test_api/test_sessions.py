def test_unauthenticated_request(test_client):
    """Prueba que una solicitud no autenticada no puede acceder a rutas protegidas."""
    response = test_client.get("/tasks/")
    assert response.status_code == 401


def test_logout(authenticated_client):
    """Prueba que un usuario pierde el acceso a rutas protegidas tras cerrar sesión."""
    client, _ = authenticated_client

    # Cerrar sesión
    response = client.get("/auth/logout")
    assert response.status_code == 302

    # Intentar acceder a una ruta protegida
    response = client.get("/tasks/")
    assert response.status_code == 401


def test_session_expired(authenticated_client):
    """Prueba que una sesión caducada devuelva un error al acceder a rutas protegidas."""
    client, _ = authenticated_client

    # Manipular la sesión para simular expiración
    with client.session_transaction() as sess:
        sess.clear()

    # Intentar acceder a una ruta protegida
    response = client.get("/tasks/")
    assert response.status_code == 401


def test_invalid_session(test_client):
    """Prueba que una sesión inválida es manejada correctamente."""
    with test_client.session_transaction() as sess:
        sess["user_id"] = 9999  # ID de usuario inexistente

    # Intentar acceder a una ruta protegida
    response = test_client.get("/tasks/")
    assert response.status_code == 401
