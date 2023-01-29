import sqlite3

# con = sqlite3.connect("workouts.db")
# cur = con.cursor()
# cur = cur.execute("CREATE TABLE IF NOT EXISTS workouts(date INTEGER NOT NULL, type TEXT NOT NULL, \
#         reps INTEGER NOT NULL, weight REAL NOT NULL)")
# cur = cur.execute("CREATE TABLE IF NOT EXISTS heatmap(date INTEGER NOT NULL, grp TEXT NOT NULL, \
#     score INTEGER NOT NULL)") #, UNIQUE (date, grp))

def openDb():
    '''
    Opens the database.
        Returns: connection to the database.
    The database consists of two tables: first is workout(int date, string exercise_name,
    int reps, float weight). The second is heatmap(int date, muscles_worked, float score). 
    The score is simply rep*sets*weight (in lbs).
    '''
    con = sqlite3.connect("workouts.db")
    cur = con.cursor()
    cur = cur.execute("CREATE TABLE IF NOT EXISTS workout(date INTEGER NOT NULL, type TEXT NOT NULL, \
        reps INTEGER NOT NULL, weight REAL NOT NULL)")
    cur = cur.execute("CREATE TABLE IF NOT EXISTS heatmap(date INTEGER NOT NULL, grp TEXT NOT NULL, \
        score INTEGER NOT NULL)")
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
    if tableNum == 0: cur.executemany("INSERT INTO workouts VALUES(?, ?, ?, ?)", data)
    elif tableNum == 1: cur.executemany("INSERT INTO heatmap VALUES(?, ?, ?)", data)
    else: raise Exception("Incorrect tableNum.")
    db.commit()
    

def __searchOptions(tableNum, date, other_query):
    '''
    Internal function for getting search options.
        Parameters:
            tableName (int): Table num: 0 for tracker, 1 for heatmap
            date (int/None): the date. Can be either an int or None
            other_query: (string/None): either muscle group (grp) for heatmap or type for the exercise
    '''
    options = ""
    if tableNum != 0 and tableNum != 1: raise Exception("Incorrect tableNum.")
    if tableNum == 0 and other_query != None: options += " type = \"" + str(other_query) + "\""
    if tableNum == 1 and other_query != None: options += " grp = \"" + str(other_query) + "\""
    if date != None: options += " date = " + str(date)
    if options != "": options = " WHERE" + options
    return options

def deleteRows(db, tableNum, date, other_query):
    '''
    Deletes rows that match the search parameters.
    '''
    cur = db.cursor()
    options = __searchOptions(tableNum, date, other_query)
    if options != None or options != "":
        if tableNum == 0: cur.execute("DELETE FROM workout" + options)
        if tableNum == 1: cur.execute("DELETE FROM heatmap" + options)

def fetchRows(db, tableNum, date, other_query):
    '''
    Returns the contents of the database for a given table for filtered rows.
    Parameters: tableNum (int): Table num: 0 for tracker, 1 for heatmap
    ''' # TODO: add all exercises mode?
    cur = db.cursor()
    searchOptions = __searchOptions(tableNum, date, other_query)

    if tableNum == 0: return cur.execute("SELECT * FROM workout" + searchOptions).fetchall()
    elif tableNum == 1: return cur.execute("SELECT * FROM heatmap" + searchOptions).fetchall()
    else: raise Exception("Incorrect tableNum.")

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
    '''
    db.close()
