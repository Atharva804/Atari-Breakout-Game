import sqlite3 # Database Module


#Function that is setting up database
def setup_database():
    conn = sqlite3.connect('game.db') #Connects to a SQLite database named "game.db" - if it does not exist it is creatd automatically
    cursor = conn.cursor() # Creates a cursor object using the connection - used to execute SQL commands
    #Execute SQL Command using the cursor - the command below will create a new table named users if it does not already exist - inside the cursor.execute = sql code
    cursor.execute(''' 
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY,
            username TEXT NOT NULL UNIQUE,
            password TEXT NOT NULL,
            email TEXT NOT NULL
        )
    ''')

    # Create Score table
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS scores (
            username TEXT NOT NULL UNIQUE,            
            score INTEGER ,
            best_score INTEGER,
            FOREIGN KEY (username) REFERENCES users (username)
        )
    ''')

     # Create Level table
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS levels (
            username TEXT NOT NULL UNIQUE,            
            level INTEGER ,
            best_level INTEGER,
            FOREIGN KEY (username) REFERENCES users (username)
        )
    ''')

     # Create User Statistics table
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS statistics (
            username TEXT NOT NULL UNIQUE,            
            total_time INTEGER ,
            bricks_broken INTEGER,
            powerup_collected INTEGER,
            FOREIGN KEY (username) REFERENCES users (username)
        )
    ''')

    conn.commit() #Saves changes made to the database 
    conn.close() #Closes the connection


def connect_to_db(tableName):
    conn = sqlite3.connect(tableName)
    cursor = conn.cursor()
    return cursor