from flask import Flask, request
import datetime

app = Flask(__name__)

@app.route('/predictTrafficJam', methods=['GET'])
def predictTrafficJam():
    today = datetime.datetime.today() 

    try:
        data = {
            'src': request.args['src'],
            'dst' : request.args['dst'],
            'dateFrom' : today,
            'dateTo' : (today - datetime.timedelta(6))
        }
        
        url = "http://road-information-service:8000/getRoadData"
        response = requests.post(url,data=data)

        return response
    except Exception as e:
        print("Database error")

@app.route('/')
def hello():
    return "Hello world"

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=8000)
