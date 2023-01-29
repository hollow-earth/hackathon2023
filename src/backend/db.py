import sqlite3

from matplotlib.pyplot import table

def openDb():
    '''
    Opens the database.
        Returns: connection to the database.
    The database consists of two tables: first is workout(int date, string exercise_name,
    int reps, float weight). The second is heatmap(int date, muscles_worked, float score). 
    The score is simply rep*sets*weight (in lbs).
    '''
    con = sqlite3.connect("workout.db")
    cur = con.cursor()
    cur = cur.execute("CREATE TABLE IF NOT EXISTS workout(date INTEGER NOT NULL, type TEXT NOT NULL, \
        reps INTEGER NOT NULL, weight REAL NOT NULL)")
    cur = cur.execute("CREATE TABLE IF NOT EXISTS heatmap(date INTEGER NOT NULL, grp TEXT NOT NULL, \
        score INTEGER NOT NULL)") #, UNIQUE (date, grp))
    return con

def addRows(data, tableNum, db):
    '''
    Adds row(s) to the database.
        Parameters: 
            data (array): List containing the rows to add. Each row should be a tuble, within a list
                tableName (int): Table num: 0 for tracker, 1 for heatmap
            db: the database to edit
        Returns: database object (sqlite)
    '''
    cur = db.cursor()
    if tableNum == 0: cur.executemany("INSERT INTO workout VALUES(?, ?, ?, ?)", data)
    elif tableNum == 1: cur.executemany("INSERT INTO heatmap VALUES(?, ?, ?)", data)
    else: raise Exception("Incorrect tableNum.")
    db.commit()
    

def deleteRows():

    pass

def fetchRows(db, tableNum, date, other_query):
    '''
    Returns the contents of the database for a given table for filtered rows.
    Parameters: tableNum (int): Table num: 0 for tracker, 1 for heatmap
    ''' # TODO: add all exercises mode?
    cur = db.cursor()
    data = []
    where = ""
    
    # Search options
    if tableNum == 0 and other_query != None: where += " type = \"" + str(other_query) + "\""
    if tableNum == 1 and other_query != None: where += " grp = \"" + str(other_query) + "\""
    if date != None: where += " date = " + str(date)
    if where != "": where = " WHERE" + where

    # Actual search
    if tableNum == 0: data = cur.execute("SELECT * FROM workout" + where).fetchall()
    elif tableNum == 1: data = cur.execute("SELECT * FROM heatmap" + where).fetchall()
    else: raise Exception("Incorrect tableNum.")
    return data

def debugPrintTable(db, tableNum):
    '''
    Prints the entire contents of the database for a given table.
    Parameters: tableNum (int): Table num: 0 for tracker, 1 for heatmap
    '''
    cur = db.cursor()
    if tableNum == 0: 
        for row in cur.execute("SELECT * FROM workout ORDER BY date").fetchall(): print(row)
    elif tableNum == 1:
        for row in cur.execute("SELECT * FROM heatmap ORDER BY date").fetchall(): print(row)
    else: raise Exception("Incorrect tableNum.")

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
# addRows(data = [(20230126,"Incline Bench Press",0,1), (20230125,"Lateral Raises",0,1)], tableNum=0, db=workout)
# debugPrintTable(db=workout, tableNum=0)
print(fetchRows(workout, 0, None, "Chest Press"))
closeDb(workout)