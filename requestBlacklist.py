import requests
import os
from dotenv import load_dotenv

load_dotenv()

abuseipdb_api_key = os.environ.get('abuseipdb_API_KEY')

# Defining the api-endpoint
url = 'https://api.abuseipdb.com/api/v2/blacklist'

querystring = {
    'limit':'500000'
}

headers = {
    'Accept': 'text/plain',
    'Key': abuseipdb_api_key
}

file = open("blacklist.txt", "w")

response = requests.request(method='GET', url=url, headers=headers, params=querystring);

# Formatted output
file.write(response.text)
file.close()