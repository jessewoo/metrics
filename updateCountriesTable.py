import mysql.connector
import os
import time 
import csv
from dotenv import load_dotenv

load_dotenv()

dbhost = os.environ.get('dbhost')
dbport = os.environ.get('dbport')
dbuser = os.environ.get('dbuser')
dbpw = os.environ.get('dbpassword')
database = os.environ.get('database')

mydb = mysql.connector.connect(
  host=dbhost,
  user=dbuser,
  port=dbport,
  password=dbpw,
  database=database
)

mycursor = mydb.cursor()
script_dir = os.path.dirname(__file__)

# Add in code and name of countries
initialCountriesList = script_dir + '/sandbox/initialListCountries.csv'
with open(initialCountriesList, 'r') as file:
  csvreader = csv.reader(file)  
  header = next(csvreader)

  for row in csvreader:
      code = row[0]
      name = row[1]
      now = time.strftime('%Y-%m-%d %H:%M:%S')
      mycursor.execute ("INSERT INTO countries (code, name, date_added) VALUES (%s, %s, %s)", (code, name, now))

# Add in code and name of countries
initialContinentList = script_dir + '/sandbox/initialListContinent.csv'
with open(initialContinentList, 'r') as file:
  csvreader = csv.reader(file)  
  header = next(csvreader)

  for row in csvreader:
      country = row[0]
      continent = row[1]
      now = time.strftime('%Y-%m-%d %H:%M:%S')
      mycursor.execute ("INSERT INTO country_continent (country, continent, date_added) VALUES (%s, %s, %s)", (country, continent, now))

mydb.commit()
mycursor.close()