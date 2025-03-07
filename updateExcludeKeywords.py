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
initialKWList = script_dir + '/sandbox/initialExcludeKeywords.csv'

with open(initialKWList, 'r') as file:
  csvreader = csv.reader(file)  
  header = next(csvreader)

  for row in csvreader:
      keyword = row[0]
      now = time.strftime('%Y-%m-%d %H:%M:%S')
      mycursor.execute ("INSERT INTO exclude_bot_keywords (keyword, date_added) VALUES (%s, %s)", (keyword, now))

mydb.commit()
mycursor.close()
