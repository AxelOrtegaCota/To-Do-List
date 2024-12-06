from flask import Flask, redirect, url_for
from app import create_app, db
from app.models.user import User
from app.models.task import Task

app = create_app()

@app.route('/')
def index():
    return redirect(url_for('auth.login'))  # Redirige al login

if __name__ == '__main__':
    with app.app_context():
        db.create_all()
    app.run(debug=True)
