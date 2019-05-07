from flask import Flask, request

app = Flask(__name__)

@app.route('/getRoadData', methods=['GET'])
def getRoadData():
    try:
        data = {
            'src': #request.args['src'],
            'dst' : #request.args['dst'],
            'dateFrom' : #request.args['dateFrom'],
            'dateTo' : #request.args['dateTo']
        }
        url = "http://database-service:8000/store"
        response = requests.post(url,data=data)
        print(response)

        return response
    except Exception as e:
        print("Database error")


@app.route('/')
def hello():
    return "Hello world"

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=8000)
