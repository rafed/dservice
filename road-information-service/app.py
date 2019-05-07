from flask import Flask
import requests


app = Flask(__name__)

@app.route('/getRoadData', methods=['GET'])
def getRoadData():
    try:
        data = {
            'src': "Adarsh Nagar Main Road", #request.args['src'],
            'dst' : "Ashoka Road/Shah Alam Bandh Marg/Jahangirpuri Main Road" ,#request.args['dst'],
            'dateFrom' : "07-05-2019", #request.args['dateFrom'],
            'dateTo' : "07-05-2019" #request.args['dateTo']
        }
        print(data)
        url = "http://172.16.21.70:9999/retrieve"
        response = requests.post(url,data=data)
        # print(response.text)

        return response
    except Exception as e:
        print(e)

getRoadData()
# @app.route('/')
# def hello():
#     return "Hello world"

# if __name__ == "__main__":
#     app.run(host='0.0.0.0', port=8000)
