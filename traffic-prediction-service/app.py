from flask import Flask, request
import requests
import datetime
import pandas as pd
import json
from flask_cors import CORS

app = Flask(__name__)
CORS(app)

def make_test_data(date):
    start = datetime.datetime.strptime('12:00', '%H:%M')
    
    times = []
    times.append(start.strftime('%H:%M'))
    for i in range(60,60*24,60):
        times.append((start+datetime.timedelta(minutes=i)).strftime('%H:%M'))

    weekday = datetime.datetime.strptime(date, '%d-%m-%Y').weekday()

    test_df = pd.DataFrame(columns=['weekday', 'time'])
    test_df['time'] = times
    test_df['weekday'] = weekday

    return test_df.to_json()

def make_train_data(data):
    columnNames = ['date', 'time', 'weekday', 'li', 'pc', 'src', 'dst', 'su', 'ff', 'temperature', 'daylight', 'humidity', 'raindesc', 'rainfall', 'windspeed', 'holiday', 'area', 'jf']

    df = pd.DataFrame(json.loads(data), columns=columnNames)
    print(df.head(3), flush=True)

    df = df[['time', 'weekday', 'jf']]
    print("kakakaka")
    return df.to_json()


@app.route('/predictTrafficJam', methods=['POST'])
def predictTrafficJam():
    today = datetime.datetime.today() 

    try:
        # print(request.data, flush=True)

        data = {
            'src': request.get_json().get('src'), # "Adarsh Nagar Main Road",#
            'dst' : request.get_json().get('dst'), # "Ashoka Road/Shah Alam Bandh Marg/Jahangirpuri Main Road" ,#
            'dateTo' : today.strftime('%d-%m-%Y'),
            'dateFrom' : (today - datetime.timedelta(1)).strftime('%d-%m-%Y') #(today - datetime.timedelta(6))
        }

        # print("Helllllo", flush=True)
        # print(request.get_json().get('src'), flush=True)

        road_data_url = "http://road-information-service:8000/getRoadData"
        traffic_data = requests.post(road_data_url,data=data)

        train_data = make_train_data(traffic_data.text)
        test_data = make_test_data(request.get_json().get('date')) 

        data = {
            'train': train_data,
            'test': test_data
        }

        prediction_url = "http://prediction-service:8000/predict"
        prediction = requests.post(prediction_url, data=data)

    except Exception as e:
        print(e, flush=True)

    return prediction.text
    # return json.dumps([])
    

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=8000)
