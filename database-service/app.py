from flask import Flask, request
import mysql.connector
import pickle
from datetime import datetime

app = Flask(__name__)

mydb = mysql.connector.connect(
  host="mariadb",
  user="here",
  passwd="here",
  database="here"
)

mycursor = mydb.cursor()

@app.route('/store', methods=['POST'])
def store():
    try:
        rows = pickle.loads(request.data)
        query = "insert into data values (%s" + ",%s"*17 + ")"
        mycursor.executemany(query, rows)
        mydb.commit()
    except Exception as e:
        print("Database error")
        with open("error.log.txt", "a") as error:
            s = "[%s] %s\n" % (datetime.now(), e)
            error.write(s)

    return "Done!"

@app.route('/retrieve', methods=['POST'])
def retrieve():
    try:
        src = request.args['src']
        dst = request.args['dst']
        dateFrom = request.args['dateFrom']
        dateTo = request.args['dateTo']
        query = "select * from data where src=%s and dst=%s and STR_TO_DATE(date,'%m-%d-%Y')>=STR_TO_DATE(%s,'%m-%d-%Y') and STR_TO_DATE(date,'%m-%d-%Y')<=STR_TO_DATE(%s,'%m-%d-%Y')"
        cursor.execute(query, src, dst,dateFrom, dateTo)
        result = cursor.fetchall()
        
        return result
    except Exception as e:
        print("Database error")


@app.route('/')
def hello():
    return "Hello world"

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=8000)
