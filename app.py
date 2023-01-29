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
def index():
    conn = get_db_connection()
    posts = conn.execute('SELECT * FROM posts').fetchall()
    conn.close()
    return render_template('index.html', posts=posts)
@app.route('/create/', methods=('GET', 'POST'))
def create():
    if request.method == 'POST':
        title = request.form['title']
        content = request.form['content']

        if not title:
            flash('Title is required!')
        elif not content:
            flash('Content is required!')
        else:
            conn = get_db_connection()
            conn.execute('INSERT INTO posts (title, content) VALUES (?, ?)',
                         (title, content))
            conn.commit()
            conn.close()
            return redirect(url_for('index'))

    return render_template('create.html')
@app.route('/<int:id>/edit/', methods=('GET', 'POST'))

def edit(id):
    post = get_post(id)
    if request.method == 'POST':
        title = request.form['title']
        content = request.form['content']

        if not title:
            flash('Title is required!')

        elif not content:
            flash('Content is required!')

        else:
            conn = get_db_connection()
            conn.execute('UPDATE posts SET title = ?, content = ?'
                         ' WHERE id = ?',
                         (title, content, id))
            conn.commit()
            conn.close()
            return redirect(url_for('index'))

    return render_template('edit.html', post=post)
@app.route('/<int:id>/delete/', methods=('POST',))

def delete(id):
    post = get_post(id)
    conn = get_db_connection()
    conn.execute('DELETE FROM posts WHERE id = ?', (id,))
    conn.commit()
    conn.close()
    flash('"{}" was successfully deleted!'.format(post['title']))
    return redirect(url_for('index'))

if __name__ == "__main__":
    app.run(debug=True)