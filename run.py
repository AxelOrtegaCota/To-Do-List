from flask import redirect, url_for
from app import create_app, db

# Crear la aplicación Flask
app = create_app()

# Ruta principal
@app.route('/')
def index():    
    return redirect(url_for('auth.login'))  # Redirige al login

if __name__ == '__main__':
    # Crear el contexto de la aplicación para inicializar la base de datos
    with app.app_context():
        db.create_all()  # Crea las tablas si no existen

    # Ejecutar la aplicación en modo de depuración
    app.run(debug=True)
