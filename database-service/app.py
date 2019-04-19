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
        query = "insert into data values (%s" + ",%s"*12 + ")"
        mycursor.executemany(query, rows)
        mydb.commit()
    except Exception as e:
        print("Database error")
        with open("error.log.txt", "a") as error:
            s = "[%s] %s\n" % (datetime.now(), e)
            error.write(s)

    return "Done!"
 
@app.route('/')
def hello():
    return "Hello world"

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=8000)
