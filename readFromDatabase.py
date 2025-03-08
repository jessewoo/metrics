import mysql.connector
import gzip
import os
import time
import re
from itertools import chain

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

def contains_keyword(text, keywords):
    return any(keyword in text for keyword in keywords)

script_dir = os.path.dirname(__file__)
oneCmsAuthLog = script_dir + '/sandbox/access.log-20250101v1.gz'

pattern_old = r"^(\d{4}-\d{2}-\d{2})\s+(\d+:\d{2}:\d{2})\s+([\w\-\d]+)\s+(\S+)\s+\"(.+)\"\s+([\-\d]+)\s+([\d]+)\s+([\w\-\.\d]+)\s+\"(.*)\"\s+\"(.*)\"\s+([\w\-\.\d]+)\s+([\w\-\d]+)\s+([\w\-\d]+)\s+(.*)$"
pattern_new_og = r"^(\d{4}-\d{2}-\d{2})\s+(\d+:\d{2}:\d{2})\s+([\w\-\d]+)\s+([\d]+)\s+(\S+)\s+\"(.+)\"\s+([\-\d]+)\s+([\d]+)\s+([\w\-\.\d]+)\s+\"(.*)\"\s+\"(.*)\"\s+([\w\-\.\d]+)\s+([\w\-\d]+)\s+([\w\-\d]+)\s+([\-\d]+)\s+([^_].*)\s+([^_].*)\s+([^_].*)\s+([^_].*)\s+([^_].*)\s+([^_].*)\s+([^_].*)\s+([^_].*)$";

# ------- DATABASE CALLS ----------
# Exclude Bot Keywords
mySqlBotKws = mydb.cursor()
mySqlBotKws.execute ("SELECT keyword FROM exclude_bot_keywords")
entries = mySqlBotKws.fetchall()
arrayOfExcludeKeywords = list(chain(*entries))
mySqlBotKws.close()

# Exclude IP Addresses
mySqlIPAddresses = mydb.cursor()
mySqlIPAddresses.execute ("SELECT ip_address FROM exclude_ip_list WHERE status=1")
ipentries = mySqlIPAddresses.fetchall()
arrayOfExcludeIpAddresses = list(chain(*ipentries))
print(arrayOfExcludeIpAddresses)
mySqlIPAddresses.close()

# Keep an array of keywords and ip addresses to ignore from database
userAgentFilterOut = arrayOfExcludeKeywords
ipAddressesFilterOut = arrayOfExcludeIpAddresses
blackListIp = script_dir + '/ipaddressNetwork.txt'

ipAddressesFilterOutExtra = []
with open(blackListIp, 'r') as file:
  # Read all lines into a list
  lines = file.readlines()
  ipAddressesFilterOutExtra = [line.strip() for line in lines]

firstLineFilterOut = ['task=diskusage']

# fileRemaining = open("remainingAccessLogs.txt", "w")

with gzip.open(oneCmsAuthLog, 'rt') as file:
  nomatchCnt = 0; newogmatchCnt = 0;
  baduserAgents = 0; badIpAddresses = 0; badUrls = 0;

  mySqlInsertAccessLog = mydb.cursor()

  for idx, line in enumerate(file):
    newogMatch = re.match(pattern_new_og, line)

    if newogMatch:
      datestamp   = newogMatch.group(1)
      timestamp   = newogMatch.group(2)
      timezone    = newogMatch.group(3)
      pid         = newogMatch.group(4)
      user        = newogMatch.group(5)
      firstline   = newogMatch.group(6)
      returnLine  = newogMatch.group(7)
      bytes       = newogMatch.group(8)
      ip_address  = newogMatch.group(9)
      referrer    = newogMatch.group(10)
      useragent   = newogMatch.group(11)
      sslport     = newogMatch.group(12)
      ts          = newogMatch.group(13)
      tms         = newogMatch.group(14)
      uidNumber   = newogMatch.group(15)
      joomla_id   = newogMatch.group(16)
      st_cookie   = newogMatch.group(17)
      auth_type   = newogMatch.group(18)
      comp_name   = newogMatch.group(19)
      view_name   = newogMatch.group(20)
      task_name   = newogMatch.group(21)
      actn_name   = newogMatch.group(22)
      item_name   = newogMatch.group(23)

      if contains_keyword(useragent.lower(), arrayOfExcludeKeywords):
          # print("AGENT IS BAD: " + useragent)
          baduserAgents += 1
      elif contains_keyword(ip_address, ipAddressesFilterOutExtra) or contains_keyword(ip_address, ipAddressesFilterOut):
          # print("IP ADDRESS IS BAD: " + ip_address)
          badIpAddresses += 1
      elif contains_keyword(firstline, firstLineFilterOut):
          badUrls += 1
      else:
          # Check the remaining rows 
          # fileRemaining.write(line)
          # Need to do MORE CLEAN UP
          # print(line)
          mySqlInsertAccessLog.execute ("INSERT INTO accesslog_apache_web (session_id, date_added, ip_address, country, url_hit, user_agent, host, domain, apache_process_id) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s)", (joomla_id, datestamp + " " + timestamp, ip_address, "country", firstline, useragent, "host", "domain", pid))

      newogmatchCnt += 1  
    else:
      nomatchCnt += 1

  print('new match og:' + str(newogmatchCnt))
  print('no match:' + str(nomatchCnt))
  print('------------')
  print('bad user agents:' + str(baduserAgents))
  print('bad ip addresses:' + str(badIpAddresses))
  print('bad url:' + str(badUrls))

  mydb.commit()
  mySqlInsertAccessLog.close()
