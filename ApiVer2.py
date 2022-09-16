import pickle #pickle is a python module that allows you to serialize objects
import sqlite3
import pyrebase #prebase is used to connect to the firebase database
import datetime #This function is used to insert the data into the local database
from flask import Flask, request, render_template
#flask is used to create a web server
#Flask is a micro web framework written in Python.
# It is classified as a microframework because it does not require particular tools or libraries.
#request :  used to get the data from the firebase database
#render_template :  used to render the html page

app=Flask(__name__) #This is used to create a flask app

conf = {
    "apiKey": "AIzaSyCT1e96tqXnpUBT9T8YJq7N_goWW8LFxIU",
    "authDomain": "fakenewsdetection-a73ba.firebaseapp.com",
    "projectId": "fakenewsdetection-a73ba",
    "storageBucket": "fakenewsdetection-a73ba.appspot.com",
    "messagingSenderId": "989183519823",
    "appId": "1:989183519823:web:676ade3a4389e41a1b0e3a",
    "measurementId": "G-8KVV3H2X2L",
    "databaseURL":"https://fakenewsdetection-a73ba-default-rtdb.firebaseio.com/"
} 
#conf is used to connect to the firebase database using the api key

firebase = pyrebase.initialize_app(conf) #This is used to initialize the firebase database
db = firebase.database() #This function is used to insert the data into the local database


with open('LogisticModelVer2.pkl', 'rb') as pkl: #This is used to open the logistic model
    model = pickle.load(pkl) #This is used to load the logistic model
    
with open('tfidfVer2.pkl', 'rb') as tfidf: #This is used to open the tfidf model
    tfidf = pickle.load(tfidf) #This is used to load the tfidf model


@app.route("/predict",methods=['POST','GET'])
#This is used to create a route for the prediction
#POST :  used to get the data from the firebase database
#GET :  used to render the html page

def predict(): #This is used to create a function for the prediction
    if request.method == 'POST':
        text = request.form['news'] #This is used to get the news from the firebase database
        transformed = tfidf.transform([text]) #tfidf.transform :  used to transform the text into a vector form 
        result = model.predict(transformed)[0] #This is used to predict the news
        ct = datetime.datetime.now() #This is used to get the current time
        if result == '1':
            flag = "Real"
        
        else:
            flag = "Fake"

        data = {'Prediction Time': str(ct), 'Text':text, 'Flag':flag} 
        #This is used to store the data in the dictionary
        insertIntoLocalDB(data) #This is used to insert the data into the local database
        db.child("Predictions").push(data) #This is used to push the data into the firebase database
        print(flag) #This is used to print the flag
        return render_template('result.html', flag= flag) #This is used to render the html page
    
    else: #if the request is get
        predictions = db.child("Predictions").get().each() 
        #To get the data from the firebase database
        #each() :  used to get the data from the firebase database
        return render_template('data.html', predictions=predictions)
        #This is used to render the html page 
        #predictions=predictions :  used to get the data from the firebase database

@app.route('/') #This is used to create a route for the home page
def home():
	return render_template('home.html') 


def insertIntoLocalDB(dictionary): #This is used to create a function to insert the data into the local database
    local_db = sqlite3.connect('predictions.db') #This is used to connect to the local database
    local_db.execute(f"INSERT INTO PREDICTIONS(CREATION_TIME, TEXT_BODY, FLAG)"
             f"VALUES ('{dictionary['Prediction Time']}', '{dictionary['Text']}', '{dictionary['Flag']}')")
    #execute :  used to execute the query
    #INSERT INTO PREDICTIONS(CREATION_TIME, TEXT_BODY, FLAG) :  used to insert the data into the local database
    
    local_db.commit() #This is used to commit the changes
    local_db.close() #This is used to close the connection


if __name__=='__main__': #This is used to run the flask app
    app.run() 