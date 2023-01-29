import sqlite3
import numpy as np

def openDb():
    '''
    Opens the database.
        Returns: connection to the database.
    '''
    con = sqlite3.connect("workout.db")
    cur = con.cursor()
    cur = cur.execute("CREATE TABLE IF NOT EXISTS workout(date INTEGER NOT NULL, type TEXT NOT NULL, \
        reps INTEGER NOT NULL, weight REAL NOT NULL)")
    cur = cur.execute("CREATE TABLE IF NOT EXISTS heatmap(date INTEGER NOT NULL, grp TEXT NOT NULL, \
        frac_num REAL NOT NULL)")
        # If you have 3 sets just call add 3 lines so they can all have diff. 
        # weight and reps
    return con

def retrieveRows():
    pass

def addRows(data, tableNum, db):
    '''
    Adds row(s) to the database.
        Parameters: data (array): List containing the rows to add. Each row should be a tuble, within a list
                    tableName (int): Table num: 0 for tracker, 1 for heatmap
                    db: the database to edit
        Returns: database object (sqlite)
    '''
    cur = db.cursor()
    if tableNum == 0: 
        res = cur.execute("SELECT name FROM sqlite_master")
        print(res.fetchall())
        cur.executemany("INSERT INTO workout VALUES(?, ?, ?, ?)", data)
    elif tableNum == 1: cur.executemany("INSERT INTO heatmap VALUES(?, ?, ?)", data)
    db.commit()
    

def deleteRows():
    pass

# def debugPrintTable(db):
#     '''
#     Prints the entire contents of the database for a given table.
#     Parameters: tableNum (int): Table num: 0 for tracker, 1 for heatmap
#     '''


def closeDb(db):
    '''
    Closes the database.
        Parameters: database object: database to close
        Returns: status (bool): 0 if closed correctly
    '''
    db.close()
    db = None
    return 0

workout = openDb();
input()
addRows(data = [(20230128,"Chest Press",8,135.0)], tableNum=0, db=workout)
closeDb(workout)
input()