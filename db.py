import sqlite3
import numpy as np

def openDb():
    '''
    Opens the database.
        Returns: connection to the database.
    '''
    con = sqlite3.connect("workout.db")
    cur = con.cursor()
    if cur.fetchall() == False:
        cur.execute("CREATE TABLE workout(date, type, reps, weight)") 
        cur.execute("CREATE TABLE heatmap(group, relative_num")
        # If you have 3 sets just call add 3 lines so they can all have diff. 
        # weight and reps
    return con

def retrieveRows():
    pass

def addRows(array, tableNum, db):
    '''
    Adds row(s) to the database.
        Parameters: array (array): List containing the rows to add.
                    tableNum (int): Table number
                    db: the database to edit
        Returns: database object (sqlite)
    '''
    # cur.execute("""
    """INSERT INTO movie VALUES
        ('Monty Python and the Holy Grail', 1975, 8.2),
        ('And Now for Something Completely Different', 1971, 7.5)"""
    pass
    

def deleteRows():
    pass

def debugPrintTable(db):
    '''
    Adds row(s) to the database.
        Parameters: rowArray (array): Numpy array containing the rows to add.
                    tableNum (int): Table number
        Returns: database object (sqlite)
    '''

def closeDb(db):
    '''
    Closes the database.
        Parameters: database object: database to close
        Returns: status (bool): 0 if closed correctly
    '''
    db.close()
    return 0

workout = openDb();
addRows([20230128,"Chest Press",8,135.0])