import gzip
import os
import re
import pandas as pd

script_dir = os.path.dirname(__file__)

# extract regex match groups and append them to a Pandas DataFrame:

# Read and parse out the CMS auth log files
# Created a file that only takes the first 6 minutes of 1/1/25
oneCmsAuthLog = script_dir + '/sandbox/access.log-20250101-1m.gz'

pattern_old = r"^(\d{4}-\d{2}-\d{2})\s+(\d+:\d{2}:\d{2})\s+([\w\-\d]+)\s+(\S+)\s+\"(.+)\"\s+([\-\d]+)\s+([\d]+)\s+([\w\-\.\d]+)\s+\"(.*)\"\s+\"(.*)\"\s+([\w\-\.\d]+)\s+([\w\-\d]+)\s+([\w\-\d]+)\s+(.*)$"
pattern_new_og = r"^(\d{4}-\d{2}-\d{2})\s+(\d+:\d{2}:\d{2})\s+([\w\-\d]+)\s+([\d]+)\s+(\S+)\s+\"(.+)\"\s+([\-\d]+)\s+([\d]+)\s+([\w\-\.\d]+)\s+\"(.*)\"\s+\"(.*)\"\s+([\w\-\.\d]+)\s+([\w\-\d]+)\s+([\w\-\d]+)\s+([\-\d]+)\s+([^_].*)\s+([^_].*)\s+([^_].*)\s+([^_].*)\s+([^_].*)\s+([^_].*)\s+([^_].*)\s+([^_].*)$";

# 23 captured groups - using regex101.com in python. Broke it down - removed the / for php
pattern_new = r"^(\d{4}-\d{2}-\d{2})\s+(\d+:\d{2}:\d{2})\s+([\w\-\d]+)\s+([\d]+)\s+(\S+)\s+\"(.+)\"\s+([\-\d]+)\s+([\d]+)\s+([\w\-\.\d]+)\s+\"(.*)\"\s+\"(.*)\"\s+([\w\-\.\d]+)\s+([\w\-\d]+)\s+([\w\-\d]+)\s+([\-\d]+)\s+([^_].*)\s+([^_].*)\s+([^_].*)\s+([^_].*)\s+([^_].*)\s+([^_].*)\s+([^_].*)\s+([^_].*)$"

data = []
with gzip.open(oneCmsAuthLog, 'rt') as file:
  for idx, line in enumerate(file):
    match = re.match(pattern_new, line)
    if match:
      data.append(match.groups())

  df = pd.DataFrame(data, columns=['Datestamp', 'Timestamp', 'Timezone', 'Pid', 'User', 'Firstline', 'Return', 'Bytes', 'Ip', 'Referrer', 'Useragent', 'sslport', 'ts', 'tms', 'uidNumber', 'joomla_id', 'st_cookie', 'auth_type', 'comp_name', 'view_name', 'task_name', 'actn_name', 'item_name'])
  
  print(df)


# Utilize the entire dataframe, filter out offending referrer URL and filter out bad IP addresses
# Remaining rows - store into database - maybe that's double, not worth it
# Go row after row, determine if it's good, then push to web hits