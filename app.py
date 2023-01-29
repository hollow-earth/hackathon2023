from turtle import color
from flask import Flask, render_template, request, url_for,  redirect, abort, flash
import sqlite3
import db_manager
import matplotlib.pyplot as plt
from numpy import array, sort

debugMode = True

app = Flask(__name__)
app.config['SECRET_KEY'] = 'your secret key'

def get_db_connection(): # Untested
    conn = db_manager.openDb()
    conn = sqlite3.connect('workouts.db')
    conn.row_factory = sqlite3.Row
    return conn

def get_workout(date, other_query): # Untested, to be fixed
    conn = get_db_connection()
    data = db_manager.fetchRows(conn, 0, date, other_query)
    db_manager.closeDb(conn)
    if data is None: abort(404)
    return data

@app.route('/')
@app.route('/home')
def index(): return render_template('home.html')

@app.route('/input', methods=('GET', 'POST'))
def input():
    if request.method == 'POST':
        date = request.form["time"]
        date = int(str(date).replace("-",""))
        weight = float(request.form["weight"])
        reps = int(request.form["reps"])
        exercise = str(request.form["exercise"])

        if not date: flash("Date is required! (date)")
        elif not weight: flash("Content is required! (float)")
        elif not reps: flash("Number of reps are required (integer)")
        elif not exercise: flash("Exercise required! (string)")
        else:
            conn = db_manager.openDb()
            db_manager.addRows(db=conn, tableNum=0, data=[(date, exercise, reps, weight)])
            conn.commit()
            if debugMode: print(db_manager.debugPrintTable(conn, 0))
            db_manager.closeDb(conn)
            return redirect(url_for('data'))
    return render_template('input.html')

# @app.route('/<int:id>/edit/', methods=('GET', 'POST'))
# def edit(id):
#     # post = get_post(id)
#     # if request.method == 'POST':
#     #     title = request.form['title']
#     #     content = request.form['content']
#     #     if not title:
#     #         flash('Title is required!')

#     #     elif not content:
#     #         flash('Content is required!')
#     #     else:
#     #         conn = get_db_connection()
#     #         conn.execute('UPDATE posts SET title = ?, content = ?'
#     #                      ' WHERE id = ?',
#     #                      (title, content, id))
#     #         conn.commit()
#     #         conn.close()
#     #         return redirect(url_for('index'))
#     # return render_template('edit.html', post=post)
#     pass

@app.route('/<int:id>/delete/', methods=('POST',))
def delete(id):
    # post = get_post(id)
    # conn = get_db_connection()
    # conn.execute('DELETE FROM posts WHERE id = ?', (id,))
    # conn.commit()
    # conn.close()
    # flash('"{}" was successfully deleted!'.format(post['title']))
    # return redirect(url_for('index'))
    pass

@app.route('/muscle')
def muscle(): return render_template('muscle.html')
@app.route('/data')
def data(): 
    conn = get_db_connection()
    data = db_manager.fetchRows(conn, 0, None, None)
    db_manager.closeDb(conn)
    # data.sort() # TODO: sort by date
    return render_template('data.html', value=data)

@app.route('/progress', methods=("GET", "POST"))
def progress(): 
    if request.method == 'POST':
        exercise = request.form["exercise"]
        if not exercise: flash("Date is required! (date)")
        conn = get_db_connection()
        data = db_manager.fetchRows(conn, 0, None, str(exercise))
        db_manager.closeDb(conn)
        x_data = []
        y_data = []
        for row in data:
            x_data.append(row[0])
            y_data.append(row[2]*row[3])
        fig = plt.figure()
        plt.plot(x_data, y_data, marker="o", color="red")
        plt.title("Progression for " + str(exercise))
        plt.savefig("./static/plot.png", format="png")
        plt.close(fig)

    return render_template('progress.html')

if __name__ == "__main__":
    app.run(debug=debugMode)