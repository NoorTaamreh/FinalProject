import sqlite3

conn = sqlite3.connect('predictions.db')
#connect :  used to connect to the local database

cursor = conn.cursor() #This is used to create a cursor object to execute the query

query = """CREATE TABLE PREDICTIONS(
        CREATION_TIME CHAR(26) NOT NULL,
        TEXT_BODY TEXT NOT NULL, 
        FLAG CHAR(4) NOT NULL) 
        """
cursor.execute(query) #This is used to execute the query

conn.commit()   #This is used to commit the changes
conn.close()   #This is used to close the connection