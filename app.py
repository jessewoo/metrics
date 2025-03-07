from flask import Flask, request, jsonify, render_template
import mysql.connector
import os
import time 
from dotenv import load_dotenv
from itertools import chain

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

app = Flask(__name__)

@app.route('/')
def index():
    return 'Hello, World!'

@app.route('/about')
def about():
    return 'About Page'


# --------- API ----------
incomes = [
    {'description': 'salary', 'amount': 5000}
]

@app.route('/incomes')
def get_incomes():
    return jsonify(incomes)

@app.route('/incomes', methods=['POST'])
def add_income():
    incomes.append(request.get_json())
    return '', 204


@app.route('/exclude_keywords', methods=['GET'])
def get_exclude_keywords():
    mycursor = mydb.cursor()
    mycursor.execute ("SELECT keyword FROM exclude_bot_keywords")
    entries = mycursor.fetchall()
    arrayOfKeywords = list(chain(*entries))
    return arrayOfKeywords

@app.route('/exclude_keywords', methods=['POST'])
def add_exclude_keywords():
    mycursor = mydb.cursor()

    body = request.get_json()

    keyword = body["keyword"]
    now = time.strftime('%Y-%m-%d %H:%M:%S')
    mycursor.execute ("INSERT INTO exclude_bot_keywords (keyword, date_added) VALUES (%s, %s)", (keyword, now))
    mydb.commit()
    mycursor.close()
    return '', 204

# # Example of handling 404 errors
# @app.errorhandler(404)
# def page_not_found(e):
#     return render_template('404.html'), 404

if __name__ == '__main__':
    app.run(debug=True)