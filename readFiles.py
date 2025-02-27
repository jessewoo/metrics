import gzip
import os

script_dir = os.path.dirname(__file__)

# Read and parse out the CMS auth log files
oneCmsAuthLog = script_dir + '/files/cmsauth/cmsauth.log-20250101.gz'

with gzip.open(oneCmsAuthLog, 'rb') as f:
  file_content = f.read()
 
print(file_content)