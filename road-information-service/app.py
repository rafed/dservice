from flask import Flask, request

app = Flask(__name__)

@app.route('/getRoadData', methods=['GET'])
def getRoadData():
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
