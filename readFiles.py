import gzip
import os
import re

script_dir = os.path.dirname(__file__)

# Read and parse out the CMS auth log files
# Created a file that only takes the first 6 minutes of 1/1/25
oneCmsAuthLog = script_dir + '/sandbox/access.log-20250101-1m.gz'

pattern_old = r"^(\d{4}-\d{2}-\d{2})\s+(\d+:\d{2}:\d{2})\s+([\w\-\d]+)\s+(\S+)\s+\"(.+)\"\s+([\-\d]+)\s+([\d]+)\s+([\w\-\.\d]+)\s+\"(.*)\"\s+\"(.*)\"\s+([\w\-\.\d]+)\s+([\w\-\d]+)\s+([\w\-\d]+)\s+(.*)$"
pattern_new_og = r"^(\d{4}-\d{2}-\d{2})\s+(\d+:\d{2}:\d{2})\s+([\w\-\d]+)\s+([\d]+)\s+(\S+)\s+\"(.+)\"\s+([\-\d]+)\s+([\d]+)\s+([\w\-\.\d]+)\s+\"(.*)\"\s+\"(.*)\"\s+([\w\-\.\d]+)\s+([\w\-\d]+)\s+([\w\-\d]+)\s+([\-\d]+)\s+([^_].*)\s+([^_].*)\s+([^_].*)\s+([^_].*)\s+([^_].*)\s+([^_].*)\s+([^_].*)\s+([^_].*)$";

# 23 captured groups - using regex101.com in python. Broke it down - removed the / for php
pattern_new = r"^(\d{4}-\d{2}-\d{2})\s+(\d+:\d{2}:\d{2})\s+([\w\-\d]+)\s+([\d]+)\s+(\S+)\s+\"(.+)\"\s+([\-\d]+)\s+([\d]+)\s+([\w\-\.\d]+)\s+\"(.*)\"\s+\"(.*)\"\s+([\w\-\.\d]+)\s+([\w\-\d]+)\s+([\w\-\d]+)\s+([\-\d]+)\s+([^_].*)\s+([^_].*)\s+([^_].*)\s+([^_].*)\s+([^_].*)\s+([^_].*)\s+([^_].*)\s+([^_].*)$"

with gzip.open(oneCmsAuthLog, 'rt') as file:
  nomatchCnt = 0; newmatchCnt = 0; oldmatchCnt = 0; newogmatchCnt = 0;
  for idx, line in enumerate(file):

    oldMatch = re.match(pattern_old, line)
    newogMatch = re.match(pattern_new_og, line)
    newMatch = re.match(pattern_new, line)

    if oldMatch:
      oldmatchCnt += 1
    elif newogMatch:
      datestamp = newogMatch.group(1)
      useragent = newogMatch.group(11)
      print(useragent)
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
  
# file_content = file.read()
# print(file_content);