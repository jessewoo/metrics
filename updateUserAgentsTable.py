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
initialBotList = script_dir + '/sandbox/initialListBotUserAgents.csv'

with open(initialBotList, 'r') as file:
  csvreader = csv.reader(file)  
  header = next(csvreader)

  for row in csvreader:
      botName = row[0]
      now = time.strftime('%Y-%m-%d %H:%M:%S')
      mycursor.execute ("INSERT INTO bot_useragent (useragent, date_added) VALUES (%s, %s)", (botName, now))

mydb.commit()
mycursor.close()
