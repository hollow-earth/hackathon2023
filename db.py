import sqlite3

def openDb():
    '''
    Opens the database.
        Returns: database object (sqlite)
    '''
    con = sqlite3.connect("workout.db")
    cur = con.cursor()
    if cur.fetchall() == False:
        cur.execute("CREATE TABLE workout(date, type, reps, weight)")
    return con

def closeDb():
    '''
    Closes the database.
        Returns: status (bool): 0 if closed correctly
    '''
    con.close()
    return 0