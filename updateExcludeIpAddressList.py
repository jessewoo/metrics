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
initialIpList = script_dir + '/sandbox/initialListIpAddresses.csv'

with open(initialIpList, 'r') as file:
  csvreader = csv.reader(file)  
  header = next(csvreader)

  for row in csvreader:
      ipAddress = row[1]
      isp = row[2]
      match = row[3]
      site = 'geodynamics'
      source = row[4]
      year = row[5]
      now = time.strftime('%Y-%m-%d %H:%M:%S')
      mycursor.execute ("INSERT INTO exclude_ip_list (ip_address, isp, match_type, site, source, source_year, date_added) VALUES (%s, %s, %s, %s, %s, %s, %s)", (ipAddress, isp, match, site, source, year, now))

mydb.commit()
mycursor.close()
