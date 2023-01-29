from flask import Flask, render_template, request, url_for,  redirect, abort, flash
import sqlite3
import db

app = Flask(__name__)
app.config['SECRET_KEY'] = 'your secret key'

def get_db_connection(): # Untested
    conn = db.openDb()
    # conn = None
    # conn = sqlite3.connect('workouts.db')
    conn.row_factory = sqlite3.Row
    return conn

def get_workout(post_id): # Untested, to be fixed
    conn = get_db_connection()
    workouts = conn.execute('SELECT * FROM workouts WHERE id = ?',
                        (post_id)).fetchone()
    db.closeDb(conn)
    if workouts is None:
        abort(404)
    return workouts

@app.route('/')
def start():
    return render_template('home.html')
@app.route('/home')
def home():
    return render_template('home.html')
@app.route('/muscle')
def muscle():
    return render_template('muscle.html')
@app.route('/data')
def data():
    return render_template('data.html')
@app.route('/progress')
def progress():
    return render_template('progress.html')
@app.route('/input')
def input():
    return render_template('input.html')

if __name__ == "__main__":
    app.run(debug=True)