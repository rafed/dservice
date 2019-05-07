from flask import Flask, request
import requests


app = Flask(__name__)

@app.route('/getRoadData', methods=['POST'])
def getRoadData():
    try:
        data = {
            'src': request.form['src'],
            'dst' : request.form['dst'],
            'dateFrom' : request.form['dateFrom'],
            'dateTo' : request.form['dateTo']
        }
        print(data, flush=True)
        url = "http://database-service:8000/retrieve"
        response = requests.post(url,data=data)
        print(response.text, flush=True)

        return response.text
    except Exception as e:
        print(e, flush=True)

# getRoadData()
# @app.route('/')
# def hello():
#     return "Hello world"

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=8000)
