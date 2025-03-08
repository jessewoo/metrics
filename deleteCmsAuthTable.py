import mysql.connector
import os
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
mycursor.execute("DELETE FROM accesslog_apache_web")

mydb.commit()
mycursor.close()