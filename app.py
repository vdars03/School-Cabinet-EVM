from flask import Flask, render_template, request, redirect, url_for
import sqlite3

app = Flask(__name__)

# Database setup
DATABASE = 'database/voting.db'

def get_db_connection():
    conn = sqlite3.connect(DATABASE)
    conn.row_factory = sqlite3.Row
    return conn

def create_tables():
    conn = get_db_connection()
    with app.open_resource('database/schema.sql', mode='r') as f:
        conn.executescript(f.read())
    conn.close()

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/vote', methods=['POST'])
def vote():
    name = request.form['name']
    position = request.form['position']
    candidate = request.form['candidate']

    if not name or not position or not candidate:
        return "Please fill in all the required fields."

    conn = get_db_connection()
    cursor = conn.cursor()

    # Check if the student has already voted
    cursor.execute('SELECT * FROM votes WHERE name = ?', (name,))
    if cursor.fetchone():
        conn.close()
        return "You have already voted."

    # Save the vote in the database
    cursor.execute('INSERT INTO votes (name, position, candidate) VALUES (?, ?, ?)', (name, position, candidate))
    conn.commit()
    conn.close()

    return "Vote submitted successfully."

if __name__ == '__main__':
    create_tables()
    app.run(debug=True)
