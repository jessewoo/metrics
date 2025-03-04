import mysql.connector
import os
import time 
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

sql = "DROP TABLE bot_useragent"

mycursor.execute(sql)


# mycursor.execute("CREATE TABLE bot_useragent (id int unsigned NOT NULL AUTO_INCREMENT, useragent varchar(255) DEFAULT NULL,date_added datetime DEFAULT NULL, PRIMARY KEY (`id`)) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;")

   
# now = time.strftime('%Y-%m-%d %H:%M:%S')
# botName = 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/605.1.15 (KHTML, like Gecko; compatible; FriendlyCrawler/1.0) Chrome/120.0.6099.216 Safari/605.1.15'

# mycursor.execute ("INSERT INTO bot_useragent (useragent, date_added) VALUES (%s, %s)", (botName, now))
# mydb.commit()
# mycursor.close()
