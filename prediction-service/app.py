from flask import Flask, request
import requests
import datetime
import pandas as pd
import json
import numpy as np
from sklearn.svm import SVR

app = Flask(__name__)

@app.route('/predict', methods=['POST'])
def predictTrafficJam():
    try:
        train = pd.read_json(request.form['train'])
        test = pd.read_json(request.form['test']) # pd.read_json

        # unique_time = pd.unique(train[['time']].values.ravel('K'))
        # unique_time = sorted(unique_time)

        # dic = {}
        # i=0
        # for t in unique_time:
        #     dic[t] = i
        #     i=i+1

        ## train['weekday'] = train['weekday'].astype("category").cat.codes
        # train['time'] = train['time'].map(dic) 
        # test['time'] = test['time'].map(dic) 

        print("Before cat", flush=True)

        train['time'] = train['time'].astype("category").cat.codes
        test['time'] = test['time'].astype("category").cat.codes

        print("After cat", flush=True)

        train_x, train_y = train[['time', 'weekday']], train['jf']
        svr_rbf = SVR(kernel='rbf', C=1e3, gamma=0.1)
        model = svr_rbf.fit(train_x, train_y)

        print("after fitting", flush=True)

        print(train.head(), flush=True)
        print(test.head(), flush=True)

        predicted = model.predict(test)

        return json.dumps(np.array(predicted).tolist())
    except Exception as e:
        print(e, flush=True)

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=8000)
