import sqlite3

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
        frac_num REAL NOT NULL)") #, UNIQUE (date, grp))
        # If you have 3 sets just call add 3 lines so they can all have diff. 
        # weight and reps
    return con

def addRows(data, tableNum, db):
    '''
    Adds row(s) to the database.
        Parameters: data (array): List containing the rows to add. Each row should be a tuble, within a list
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

def retrieveRows():
    pass

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
addRows(data = [(20230128,"Chest Press",0,1), (20230128,"Chest Press",0,1)], tableNum=0, db=workout)
debugPrintTable(db=workout, tableNum=0)
closeDb(workout)