# Metrics Prototype
Prototyping a cron that will read, store and then creating a simple API that will help display metrics on the client side
CRUD platform to add ip addresses that are bad bots, LLM bots

## Architecture
### Read the Log files, parse then store to database
* Read the log files from the different directories, daily. 
* Parse thru the log files, ignoring bots
* Get the filtered list and store into database

### Create an API, show on a page
* Using FLASK API, create a simple API that will aggregate data sets
* Different API include:
    * GET and POST for bots CRUD page. With new POST, it will delete rows from the usage table
    * GET metric data by dates
* Creation of a CRUD page of bots
* Creation of a bar charts of metrics, pulling data from API with simple fetch JS 

## References
### Different log files
* /var/log/hubzero/imported/ CONTAINS all the cmsauth.log-2025*.gz
* /var/log/apache2/imported/ CONTAINS all the SITE-access.log-2025*.gz

Test files are located in files/accesslogs and files/cmsauth

## Packages
 ~~~
 python3 -m venv .venv
 source .venv/bin/activate
 pip install requests
 pip install dotenv
 pip install pandas
 pip install mysql-connector-python

 get on (.venv)
 exit: deactivate
 ~~~


Add access.log files to DB table, 
Create a function that will clean things up
Create a table with ip addresses to 



Exclude bot and nondesirable records?
userlogin
    where: import/xlogimport_authlog.php
    at insert time, exclude any IPs specified in exclude_list table
web table
    where: import/xlogimport_apache.php
    at insert time, exclude IPs, URLs, useragents specified in exclude_list table
        and useragents found in bot_useragents table (botcheck)
webhits table
    where: import/xlogimport_webhits.php
    at insert time, exclude IPs, URLs, useragents specified in exclude_list table
        and useragents found in bot_useragents table (botcheck)
websessions table
    where:  logfix_session.pl
    processes sessions from the web table, no bot checks used
jos_session_geo (whoisonline)
    where: xlogfix_whoisonline.php
    labels as bot any useragent found in bot_useragents table (botcheck)

useragent strings - put into exclude list, don't go into the web table. Exclude them to the web table. 
Userlogin