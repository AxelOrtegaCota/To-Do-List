from flask import Flask, render_template, request, redirect, url_for, flash
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager, UserMixin, login_user, logout_user, login_required, current_user
from werkzeug.security import generate_password_hash, check_password_hash
from werkzeug.utils import secure_filename
import os

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///db.sqlite'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['UPLOAD_FOLDER'] = 'static/uploads'
app.config['SECRET_KEY'] = 'mysecret'
db = SQLAlchemy(app)

# Flask-Login configuration
login_manager = LoginManager(app)
login_manager.login_view = 'login'

# Allowed image extensions
ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'gif'}

# User model for login
class User(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(100), unique=True, nullable=False)
    password = db.Column(db.String(100), nullable=False)

# Todo model for tasks
class Todo(db.Model):
    task_id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)  # Foreign key to link to user
    name = db.Column(db.String(100), nullable=False)
    image = db.Column(db.String(100))  # Path to the uploaded image
    done = db.Column(db.Boolean, default=False)

# Check allowed file types
def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

# Flask-Login user loader
@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

# Register route
@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        hashed_password = generate_password_hash(password, method='sha256')

        user = User.query.filter_by(username=username).first()
        if user:
            flash('El usuario ya existe.')
            return redirect(url_for('register'))

        new_user = User(username=username, password=hashed_password)
        db.session.add(new_user)
        db.session.commit()
        flash('Usuario registrado con éxito. Ahora puedes iniciar sesión.')
        return redirect(url_for('login'))

    return render_template('register.html')

# Login route
@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        user = User.query.filter_by(username=username).first()
        if user and check_password_hash(user.password, password):
            login_user(user)
            return redirect(url_for('home'))
        flash('Login incorrecto, por favor inténtalo de nuevo.')
    return render_template('login.html')

# Home route (To-Do List)
@app.route('/')
@login_required
def home():
    todo_list = Todo.query.filter_by(user_id=current_user.id).all()
    return render_template('base.html', todo_list=todo_list)

# Add task route with image upload
@app.route('/add', methods=['POST'])
@login_required
def add():
    name = request.form.get("name")
    file = request.files.get('file')
    filename = None

    if file and allowed_file(file.filename):
        filename = secure_filename(file.filename)
        file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))

    new_task = Todo(name=name, image=filename, user_id=current_user.id, done=False)
    db.session.add(new_task)
    db.session.commit()
    return redirect(url_for("home"))

# Update task route (mark as done/not done)
@app.route('/update/<int:todo_id>')
@login_required
def update(todo_id):
    todo = Todo.query.get(todo_id)
    if todo.user_id == current_user.id:
        todo.done = not todo.done
        db.session.commit()
    return redirect(url_for("home"))

# Delete task route
@app.route('/delete/<int:todo_id>')
@login_required
def delete(todo_id):
    todo = Todo.query.get(todo_id)
    if todo.user_id == current_user.id:
        if todo.image:
            image_path = os.path.join(app.config['UPLOAD_FOLDER'], todo.image)
            if os.path.exists(image_path):
                os.remove(image_path)
        db.session.delete(todo)
        db.session.commit()
    return redirect(url_for("home"))

# Logout route
@app.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('login'))

# Create the database tables
if __name__ == '__main__':
    with app.app_context():
        db.create_all()
    app.run(debug=True)
