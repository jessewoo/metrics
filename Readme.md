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
 - GET and POST for bots CRUD page. With new POST, it will delete rows from the usage table
 - GET metric data by dates
* Creation of a CRUD page of bots
* Creation of a bar charts of metrics, pulling data from API with simple fetch JS 

## References
### What are the different log files
* /var/log/httpd/ - Contains the apache web server access_log and error_log and related virtual hosts logs if set up to log here. 
* /var/log/apache2 - Contains the apache web server access_log and error_log and related virtual hosts logs if set up to log here.