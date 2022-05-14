from flask import Flask, request, jsonify
import requests
import threading
import sqlite3
import os
import pandas as pd
import time

app = Flask(__name__)

# Constants 
COLUMNS        = ['iso_code','location','date','total_cases', 'new_cases', 'total_deaths', 'new_deaths', 'total_tests', 'new_tests', 'total_vaccinations', 'people_vaccinated', 'people_fully_vaccinated', 'new_vaccinations']
REPOSITORY_URL = "https://raw.githubusercontent.com/owid/covid-19-data/master/public/data/" 
FILE_NAME      = "owid-covid-data.csv"
LOC_FILE_NAME  = "Location.csv"
DATABASE_NAME  = "covid_data.db"
CURRENT_DIR    = os.getcwd() + "/app/"
CHUNK_SIZE     = 5000
CSV_CHUNK_SIZE = 10000

# Queries
CREATE_TABLE_SQL = 'CREATE TABLE covid (iso_code                  TEXT , \
                                            location                  TEXT , \
                                            date                      DATE , \
                                            total_cases               NUMBER, \
                                            new_cases                 NUMBER, \
                                            total_deaths              NUMBER, \
                                            new_deaths                NUMBER, \
                                            total_tests               NUMBER, \
                                            new_tests                 NUMBER, \
                                            total_vaccinations        NUMBER, \
                                            people_vaccinated         NUMBER, \
                                            people_fully_vaccinated   NUMBER, \
                                            new_vaccinations          NUMBER)'
DELETE_TABLE_SQL = 'DROP TABLE IF EXISTS covid'
INSERT_TABLE_SQL = 'INSERT INTO covid VALUES(?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)'

CREATE_LOCATION_SQL = 'CREATE TABLE location (name       TEXT, \
                                              latitude   REAL, \
                                              longitude REAL)'
DELETE_LOCATION_SQL = 'DROP TABLE IF EXISTS location'
INSERT_LOCATION_SQL = 'INSERT INTO location VALUES (?, ?, ?)'

# Initial tasks
sqlConnection = sqlite3.connect(CURRENT_DIR + DATABASE_NAME, check_same_thread = False)
sqlCursor     = sqlConnection.cursor()

def executeQuery(query):
    sqlCursor.execute(query)
    sqlConnection.commit()

def exportAsDB():
    executeQuery(DELETE_TABLE_SQL)
    executeQuery(CREATE_TABLE_SQL)
    count = 1
    for chunk in pd.read_csv(CURRENT_DIR + FILE_NAME, chunksize = CSV_CHUNK_SIZE):
        chunk = chunk[COLUMNS].fillna(0).T
        for row in chunk:
            sqlCursor.execute(INSERT_TABLE_SQL, tuple(i for i in chunk[row]))
        print("Completed Insertions: ", count*CSV_CHUNK_SIZE)
        count += 1
    sqlConnection.commit()
    print("Successfully Completed Covid Database Work")

def exportLocationsAsDB():
    executeQuery(DELETE_LOCATION_SQL)
    executeQuery(CREATE_LOCATION_SQL)
    for chunk in pd.read_csv(CURRENT_DIR + LOC_FILE_NAME, chunksize = CSV_CHUNK_SIZE):
        chunk = chunk[["name", "latitude", "longitude"]].T
        for row in chunk:
            sqlCursor.execute(INSERT_LOCATION_SQL, tuple(i for i in chunk[row]))
    sqlConnection.commit()
    print("Successfully Completed Location Database Work")

def update(overWrite = 0):
    while True:
        print("Updating the Data in Server")
        createDB(overWrite)
        print("Update Completed Successfully")
        if not overWrite:overWrite = 1
        time.sleep(21600)

def createDB(overWrite):
    if(not overWrite and os.path.isfile(CURRENT_DIR + FILE_NAME)):
        print("File Already Exists")
    else:
        print("Working Awesome...")
        downloadRequest = requests.get(REPOSITORY_URL + FILE_NAME, stream = True)
        with open(CURRENT_DIR + FILE_NAME, 'wb') as csvFile:
            for chunk in downloadRequest.iter_content(CHUNK_SIZE):
                print("Download in Progress....")
                csvFile.write(chunk)
        print("File Downloaded Successfully")
        exportAsDB()
        exportLocationsAsDB()

@app.route('/')
def hello_world():
    return 'Hello World'

@app.route('/getCountries', methods=['GET'])
def getCountries():
    sqlCursor.execute('SELECT DISTINCT location FROM covid ASC')
    result = {"location":[i[0] for i in sqlCursor.fetchall()]}
    return jsonify(result)

@app.route('/getGraphData', methods=['POST'])
def generateGraphData():
    requestData = request.json
    query = 'SELECT %s FROM covid WHERE location="%s" AND date>="%s" AND date<"%s"'%(",".join(requestData["columns"]), requestData["location"], requestData["from"], requestData["to"])
    sqlCursor.execute(query)
    responseData = {"data":sqlCursor.fetchall()}
    return jsonify(responseData)

@app.route('/getMapData', methods=['POST'])
def generateMapData():
    requestData = request.json
    query = 'SELECT location, latitude, longitude, %s FROM covid INNER JOIN location ON covid.location = location.name WHERE date="%s"'%(",".join(requestData["columns"]), requestData["date"])
    sqlCursor.execute(query)
    responseData = jsonify({"data":sqlCursor.fetchall()})
    return responseData
 
def main():
    print("Starting Main..." + os.getcwd())
    t = threading.Thread(target = update)
    t.start()

main()
