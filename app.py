from flask import Flask, render_template, request, redirect, url_for, flash, session
from werkzeug.security import generate_password_hash, check_password_hash
import sqlite3

app = Flask(__name__)
app.secret_key = 'clave_secreta'

def init_db():
    conn = get_db_connection()
    
    conn.executescript('''
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            username TEXT NOT NULL,
            password TEXT NOT NULL
        );

        CREATE TABLE IF NOT EXISTS tasks (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            user_id INTEGER,
            content TEXT NOT NULL,
            priority TEXT NOT NULL DEFAULT 'Medium',
            image TEXT,
            FOREIGN KEY (user_id) REFERENCES users(id)
        );
    ''')

    cursor = conn.execute("PRAGMA table_info(tasks)")
    columns = [column[1] for column in cursor.fetchall()]

    if 'image' not in columns:
        conn.execute("ALTER TABLE tasks ADD COLUMN image TEXT")
        conn.commit()

    conn.close()


def get_db_connection():
    conn = sqlite3.connect('database.db')
    conn.row_factory = sqlite3.Row
    return conn


@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        hashed_password = generate_password_hash(password)

        conn = get_db_connection()
        conn.execute("INSERT INTO users (username, password) VALUES (?, ?)", (username, hashed_password))
        conn.commit()
        conn.close()

        flash('Registro exitoso. Ahora puedes iniciar sesión.')
        return redirect(url_for('login'))

    return render_template('register.html')


@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']

        conn = get_db_connection()
        user = conn.execute('SELECT * FROM users WHERE username = ?', (username,)).fetchone()
        conn.close()

        if user and check_password_hash(user['password'], password):
            session['user_id'] = user['id']
            session['username'] = user['username']
            return redirect(url_for('todo_list'))
        else:
            flash('Usuario o contraseña incorrectos')

    return render_template('login.html')


@app.route('/todo', methods=['GET', 'POST'])
def todo_list():
    if 'user_id' not in session:
        return redirect(url_for('login'))

    conn = get_db_connection()
    user_id = session['user_id']

    if request.method == 'POST':
        task_content = request.form['task_content']
        task_priority = request.form['task_priority']
        if task_content:
            conn.execute('INSERT INTO tasks (user_id, content, priority) VALUES (?, ?, ?)', (user_id, task_content, task_priority))
            conn.commit()

    tasks = conn.execute('SELECT * FROM tasks WHERE user_id = ?', (user_id,)).fetchall()
    conn.close()

    return render_template('todo.html', tasks=tasks)

@app.route('/edit_task/<int:task_id>', methods=['POST'])
def edit_task(task_id):
    if 'user_id' not in session:
        return redirect(url_for('login'))

    new_content = request.form['new_content']
    new_priority = request.form['new_priority']
    conn = get_db_connection()
    conn.execute('UPDATE tasks SET content = ?, priority = ? WHERE id = ?', (new_content, new_priority, task_id))
    conn.commit()
    conn.close()

    return redirect(url_for('todo_list'))

@app.route('/delete_task/<int:task_id>', methods=['POST'])
def delete_task(task_id):
    if 'user_id' not in session:
        return redirect(url_for('login'))

    conn = get_db_connection()
    conn.execute('DELETE FROM tasks WHERE id = ?', (task_id,))
    conn.commit()
    conn.close()

    return redirect(url_for('todo_list'))


@app.route('/logout')
def logout():
    session.pop('user_id', None)
    session.pop('username', None)
    flash('Has cerrado sesión.')
    return redirect(url_for('login'))

if __name__ == '__main__':
    init_db()
    app.run(debug=True)
