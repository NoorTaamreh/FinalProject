import sqlite3
conn = sqlite3.connect('predictions.db') #This is used to connect to the local database
cursor = conn.execute("SELECT * from PREDICTIONS")  #To get all the data from the local database
print(cursor.fetchall()) #This is used to print all the data from the local database
conn.close() #This is used to close the connection