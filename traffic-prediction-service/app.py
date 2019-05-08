from flask import Flask, request
import requests
import datetime

app = Flask(__name__)

@app.route('/predictTrafficJam', methods=['POST'])
def predictTrafficJam():
    today = datetime.datetime.today() 

    try:
        data = {
            'src': "Adarsh Nagar Main Road",#request.form['src'],
            'dst' : "Ashoka Road/Shah Alam Bandh Marg/Jahangirpuri Main Road" ,#request.form['dst'],
            'dateTo' : today.strftime('%d-%m-%Y'),
            'dateFrom' : (today - datetime.timedelta(1)).strftime('%d-%m-%Y') #(today - datetime.timedelta(6))
        }
        
        url = "http://172.16.21.70:9999/getRoadData"
        response = requests.post(url,data=data)
        print(response.text)
        
        date = request.form['date']

        # columnNames = ['date', 'time', 'weekday', 'li', 'pc', 'src', 'dst', 'su', 'ff', 'temperature', 'daylight', 'humidity', 'raindesc', 'rainfall', 'windspeed', 'holiday', 'area', 'jf']
        # pd.DataFrame(response, columns=columnNames)

        return response
    except Exception as e:
        print(e)

@app.route('/')
def hello():
    return "Hello world"

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=8000)
