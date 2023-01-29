DROP TABLE IF EXISTS workouts;

CREATE TABLE workouts (
    date INTEGER NOT NULL, 
    type TEXT NOT NULL,
    reps INTEGER NOT NULL, 
    weight REAL NOT NULL
);
