from flask import Flask, render_template, request, redirect, url_for, jsonify
import sqlite3

app = Flask(__name__)

# Crear o conectar a la base de datos
def init_db():
    conn = sqlite3.connect('tasks.db')
    cursor = conn.cursor()
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS tasks (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            client_name TEXT NOT NULL,
            latitude REAL NOT NULL,
            longitude REAL NOT NULL
        )
    ''')
    conn.commit()
    conn.close()

# Ruta principal
@app.route('/')
def index():
    conn = sqlite3.connect('tasks.db')
    cursor = conn.cursor()
    cursor.execute('SELECT * FROM tasks')
    tasks = cursor.fetchall()
    conn.close()
    return render_template('index.html', tasks=tasks)

# Ruta para obtener tareas en formato JSON
@app.route('/tasks')
def get_tasks():
    conn = sqlite3.connect('tasks.db')
    cursor = conn.cursor()
    cursor.execute('SELECT * FROM tasks')
    tasks = cursor.fetchall()
    conn.close()
    return jsonify(tasks)  # Devolver las tareas en formato JSON

# Agregar nueva tarea
@app.route('/add', methods=['POST'])
def add_task():
    client_name = request.form['client_name']
    coordinates = request.form['coordinates']
    latitude, longitude = map(float, coordinates.split(','))  # Separar latitud y longitud
    
    conn = sqlite3.connect('tasks.db')
    cursor = conn.cursor()
    cursor.execute('INSERT INTO tasks (client_name, latitude, longitude) VALUES (?, ?, ?)', 
                   (client_name, latitude, longitude))
    conn.commit()
    conn.close()
    
    return redirect(url_for('index'))

# Eliminar tarea
@app.route('/delete/<int:id>')
def delete_task(id):
    conn = sqlite3.connect('tasks.db')
    cursor = conn.cursor()
    cursor.execute('DELETE FROM tasks WHERE id = ?', (id,))
    conn.commit()
    conn.close()
    return redirect(url_for('index'))

if __name__ == '__main__':
    init_db()  # Iniciar la base de datos
    app.run(debug=True)
