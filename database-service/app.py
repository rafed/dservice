from flask import Flask, request
import mysql.connector
import pickle
from datetime import datetime
import json

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
    result = "asdf"

    try:
        print("pola",flush=True)

        # src = request.args.get('src')
        # dst = request.args.get('dst')
        # dateFrom = request.args.get('dateFrom')
        # dateTo = request.args.get('dateTo')

        src = request.form['src']
        dst = request.form['dst']
        dateFrom = request.form['dateFrom']
        dateTo = request.form['dateTo']

        print("jajajaja", src,dst,dateFrom,dateTo,flush=True)

        query = "select * from data where src=%s and dst=%s and STR_TO_DATE(date,'%d-%m-%Y')>=STR_TO_DATE(%s,'%d-%m-%Y') and STR_TO_DATE(date,'%d-%m-%Y')<=STR_TO_DATE(%s,'%d-%m-%Y')"
        mycursor.execute(query, [src, dst, dateFrom, dateTo])
        result = mycursor.fetchall()
        
        print("khajna", result,flush=True)
    except Exception as e:
        print("Database error ", e, flush=True)

    return json.dumps(result)

@app.route('/')
def hello():
    return "Hello world"

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=8000)
