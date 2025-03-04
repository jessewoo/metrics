import gzip
import os
import re

def contains_keyword(text, keywords):
    return any(keyword in text for keyword in keywords)

script_dir = os.path.dirname(__file__)

# Read and parse out the CMS auth log files
# Created a file that only takes the first 6 minutes of 1/1/25
oneCmsAuthLog = script_dir + '/sandbox/access.log-20250101v1.gz'

pattern_old = r"^(\d{4}-\d{2}-\d{2})\s+(\d+:\d{2}:\d{2})\s+([\w\-\d]+)\s+(\S+)\s+\"(.+)\"\s+([\-\d]+)\s+([\d]+)\s+([\w\-\.\d]+)\s+\"(.*)\"\s+\"(.*)\"\s+([\w\-\.\d]+)\s+([\w\-\d]+)\s+([\w\-\d]+)\s+(.*)$"
pattern_new_og = r"^(\d{4}-\d{2}-\d{2})\s+(\d+:\d{2}:\d{2})\s+([\w\-\d]+)\s+([\d]+)\s+(\S+)\s+\"(.+)\"\s+([\-\d]+)\s+([\d]+)\s+([\w\-\.\d]+)\s+\"(.*)\"\s+\"(.*)\"\s+([\w\-\.\d]+)\s+([\w\-\d]+)\s+([\w\-\d]+)\s+([\-\d]+)\s+([^_].*)\s+([^_].*)\s+([^_].*)\s+([^_].*)\s+([^_].*)\s+([^_].*)\s+([^_].*)\s+([^_].*)$";

# 23 captured groups - using regex101.com in python. Broke it down - removed the / for php
pattern_new = r"^(\d{4}-\d{2}-\d{2})\s+(\d+:\d{2}:\d{2})\s+([\w\-\d]+)\s+([\d]+)\s+(\S+)\s+\"(.+)\"\s+([\-\d]+)\s+([\d]+)\s+([\w\-\.\d]+)\s+\"(.*)\"\s+\"(.*)\"\s+([\w\-\.\d]+)\s+([\w\-\d]+)\s+([\w\-\d]+)\s+([\-\d]+)\s+([^_].*)\s+([^_].*)\s+([^_].*)\s+([^_].*)\s+([^_].*)\s+([^_].*)\s+([^_].*)\s+([^_].*)$"

# Need to store this into a database table or a csv file
userAgentFilterOut = ['semrush','bot','robot','paessler','petalsearch','spider','sogou','gsa-purdue-crawler','facebookexternal','crawler','compute.amazonaws.com', 'fbsv.net', 'facebook', 'bot.com','searchbot'
                      'crawl','googlebot','yandex','turnitin','tpiol','ask.com','baidu','naver','seznam','monsido''babbar','scrapy.org','ninja','dataforseo', 'moz.com', 'openai.com', 'gpbot', 'twitterbot']

# Pattern of ip address, general capture - get the NETWORK, ignore the port numbers
ipAddressesFilterOut2025 = [
                        '132.249.203.115', #San Diego Supercomputer
                        '51.222.253.', #Dmytro
                        '35.160.27.221', #Amazon
                        '154.54.249.193', #Babbar
                        '66.249.73.', #Google
                        '66.249.79.', #Google
                        '66.249.68.', #Google
                        '66.249.74.', #Google
                        '66.249.72.', #Google
                        '66.249.64.', #Google
                        '114.119.135.', #Huawei
                        '114.119.157.', #Huawei
                        '114.119.135.', #Huawei
                        '114.119.152.', #Huawei
                        '114.119.151.', #Huawei
                        '114.119.146.', #Huawei
                        '114.119.154.', #Huawei
                        '114.119.133.', #Huawei
                        '217.113.194.', #L'ile aux surfers
                        '185.191.171', #SEM Rush
                        '85.208.96.', #SEM Rush
                        '85.208.98.', #SEM Rush
                        '216.244.66.', #Wowrack.com
                        '108.61.246.134', #Vultr Holdings
                        '34.59.185.57', #Google LLC
                        '104.155.151.119', #Google LLC
                        '157.90.91.229', #Hetzner Online
                        '81.167.26.57', #Lyse Tele AS
                        '195.191.219.', #VeloxServ Communications
                        '194.247.173.99', #MONOLITH
                        '47.76.114.', #Alibaba
                        '47.76.139.', #Alibaba
                        '47.76.220.', #Alibaba
                        '47.76.44', #Alibaba
                        '47.76.222.', #Alibaba
                        '47.238.13', #Alibaba
                        '47.242.77.', #Alibaba
                        '8.210.8.', #Alibaba
                        '8.219.197.', #Alibaba
                        ]

ipAddressesFilterOut2024 = [
                        '132.249.69.168', #San Diego Supercomputer
                        '57.141.3.', #Facebook Ireland
                        '69.171.249.', #Facebook Ireland
                        '34.57.129.', #Google
                        '18.218.185.', #Amazon
                        '173.252.107.', #Amazon
                        '34.215.116.', #Amazon
                        '173.252.83.', #Amazon
                        '146.70.45.', #M247 Miami Infrastructure
                        '199.47.82.', #Turnitin
                        '47.242.224.', #Alibaba
                        '47.76.209.', #Alibaba
                        '47.76.99.', #Alibaba
                        '173.252.107.', #Facebook
                        '173.252.83.', #Facebook
                        '173.252.70.', #Facebook
                        '173.252.87.', #Facebook
                        '173.252.69.', #Facebook
                        '173.252.127.', #Facebook
                        '173.252.107.', #Facebook
                        '69.171.249.', #Facebook
                        '69.171.230.', #Facebook
                        '185.191.171.', #SEM Rush
                        '162.55.85.', #Hetzner Online
                        '136.243.220.', #Dataforseo OU
                        '4.227.36.', #Microsoft
                        '216.244.66.', #Wowrack.com
                        ]

ipAddressesFilterOut2023 = [
                        '47.76.35.', #Alibaba
                        '34.212.76.', #Amazon
                        '35.87.213.', #Amazon
                        '199.47.82.', #Turnitin
                        '132.249.203.115', #San Diego Supercomputer
                        '51.222.253.', #Dmytro, Ahrefs Pte Ltd
                        '193.70.81.', #OVH SAS
                        '192.95.29.', #OVH SAS
                        '54.38.85.', #OVH SAS
                        '188.165.215.', #OVH SAS
                        '185.191.171.', #SEMrush
                        '85.208.96.', #SEMrush
                        '66.249.79.', #Google
                        '52.167.144.', #Microsoft
                        '40.77.167.', #Microsoft
                        '217.113.194.', #L'ile aux surfers
                        ]

blackListIp = script_dir + '/ipaddressNetwork.txt'

ipAddressesFilterOut2 = []
with open(blackListIp, 'r') as file:
  # Read all lines into a list
  lines = file.readlines()
  ipAddressesFilterOut2 = [line.strip() for line in lines]


firstLineFilterOut = ['task=diskusage']

# print(contains_keyword('132.249.203.115', ipAddressesFilterOut))
fileRemaining = open("remainingAccessLogs.txt", "w")

with gzip.open(oneCmsAuthLog, 'rt') as file:
  nomatchCnt = 0; newmatchCnt = 0; oldmatchCnt = 0; newogmatchCnt = 0;
  baduserAgents = 0;
  badIpAddresses = 0;
  badUrls = 0;

  for idx, line in enumerate(file):
    oldMatch = re.match(pattern_old, line)
    newogMatch = re.match(pattern_new_og, line)
    newMatch = re.match(pattern_new, line)

    if oldMatch:
      oldmatchCnt += 1
    elif newogMatch:
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

      # print(useragent)
      if contains_keyword(useragent.lower(), userAgentFilterOut):
          # print("AGENT IS BAD: " + useragent)
          baduserAgents += 1
      elif contains_keyword(ip_address, ipAddressesFilterOut2) or contains_keyword(ip_address, ipAddressesFilterOut2025) or contains_keyword(ip_address, ipAddressesFilterOut2024) or contains_keyword(ip_address, ipAddressesFilterOut2023):
          # print("IP ADDRESS IS BAD: " + ip_address)
          badIpAddresses += 1
      elif contains_keyword(firstline, firstLineFilterOut):
          badUrls += 1
      else:
          # Check the remaining rows 
          fileRemaining.write(line)
      newogmatchCnt += 1  
    elif newMatch:
      newmatchCnt += 1
    else:
      print("no match in line:" + str(idx))
      nomatchCnt += 1

  print('old match:' + str(oldmatchCnt))
  print('new match og:' + str(newogmatchCnt))
  print('new match:' + str(newmatchCnt))
  print('no match:' + str(nomatchCnt))
  print('------------')
  print('bad user agents:' + str(baduserAgents))
  print('bad ip addresses:' + str(badIpAddresses))
  print('bad url:' + str(badUrls))
  fileRemaining.close()
