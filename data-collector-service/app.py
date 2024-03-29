import requests
import json
from datetime import datetime, timedelta
import pickle

appID = "LqJ21lDTyLEeGYbu4t6K"
appCode = "JaJrcnY2K-ocT9MxyhzHqA"

coordinates = [
    ((28.747193,77.091064),(28.663211,77.1978375)),     # 1
    ((28.663211,77.091064),(28.579229,77.1978375)),     # 2
    ((28.579229,77.091064),(28.495247,77.1978375)),     # 3
    ((28.747193,77.1978375),(28.663211,77.304611)),     # 4
    ((28.663211,77.1978375),(28.579229,77.304611)),     # 5
    ((28.579229,77.1978375),(28.495247,77.304611))      # 6
    ## ((28.614439,77.144623),(28.665286,77.260580)) ## previous coord for test
]

dt = datetime.now() # - timedelta(minutes=30) not needed now. time is now delhi time
date = dt.strftime("%d-%m-%Y")
time = dt.strftime("%H:%M")
weekday = dt.today().weekday()

rows = []

def collectData():
    global rows
    area = 0
    for pointX,pointY in coordinates:
        area = area + 1

        lat1,long1=pointX
        lat2,long2=pointY

        latmid = (lat1+lat2)/2
        longmid = (long1+long2)/2

        weatherURL = "https://weather.api.here.com/weather/1.0/report.json?app_id=%s&app_code=%s&product=observation&oneobservation=true&latitude=%s&longitude=%s" % (appID, appCode, latmid, longmid)
        trafficURL = "https://traffic.api.here.com/traffic/6.2/flow.json?app_id=%s&app_code=%s&bbox=%s,%s;%s,%s" % (appID, appCode, lat1, long1, lat2, long2)  # &responseattributes=sh for getting shape

        r = requests.get(weatherURL)
        weather_data = r.text

        daylight = ""
        temperature = ""
        humidity = ""
        windspeed = ""
        rainDesc = ""
        rainfall = ""
        holiday=0

        if r.status_code != 200:
            print("Weather request error")
            with open("error.log.txt", "a") as error:
                s = "[%s] Weather request error: %s %s\n" % (datetime.now(), r.status_code, weather_data)
                error.write(s)
        else:
            try:
                weather_json = json.loads(r.text)

                observations = weather_json['observations']
                location = observations['location'][0]
                observation = location['observation'][0]

                daylight = observation['daylight']
                daylight = 0 if daylight=="D" else 1
                temperature = observation['temperature']
                humidity = observation['humidity']
                windspeed = observation['windSpeed']
                rainDesc = observation['precipitationDesc']
                rainDesc = "No rain" if rainDesc is  "" else rainDesc
                rainfall = observation['rainFall'] if 'rainFall' in observation else ""
            except Exception as e:
                with open("error.log.txt", "a") as error:
                    s = "[%s] %s\n" % (datetime.now(), e)
                    error.write(s)

                fname = str(datetime.now()) + ".weather.txt"
                with open(fname, "w") as jsonFile:
                    jsonFile.write(weather_data)

        r = requests.get(trafficURL)

        # write HERE JSON to a file
        # f = open("docs_samples/{}.area.txt".format(area), "w+")
        # d = json.loads(r.text)
        # f.write(json.dumps(d, indent=4, sort_keys=True))
        # f.close()

        if r.status_code != 200:
            print("Traffic request error")
            with open("error.log.txt", "a") as error:
                s = "[%s] Traffic request error: %s %s\n" % (datetime.now(), r.status_code, r.text)
                error.write(s)
            continue
        else:
            try:
                traffic_json = json.loads(r.text)
            except Exception as e:
                print("JSON parse error")
                with open("error.log.txt", "a") as error:
                    s = "[%s] %s\n" % (datetime.now(), e)
                    error.write(s)
                fname = str(datetime.now()) + ".traffic.txt"
                with open(fname, "w") as jsonFile:
                    jsonFile.write(r.text)
                continue

            try:
                for RWS in traffic_json['RWS']:
                    for RW in RWS['RW']:
                        for FIS in RW['FIS']:
                            LI = RW['LI']
                            dst = RW['DE']
                            for FI in FIS['FI']:
                                src = FI['TMC']['DE']
                                # LE = FI['TMC']['LE']
                                # CN = FI['CF'][0]['CN']
                                # SP = FI['CF'][0]['SP']
                                SU = FI['CF'][0]['SU']
                                FF = FI['CF'][0]['FF']
                                JF = FI['CF'][0]['JF']
                                # SHP = FI['SHP'][0]['value'][0]
                                PC = FI['TMC']['PC']
                            
                                if "-" in LI:
                                    src,dst = dst,src

                                row =   (date, time, weekday, \
                                        LI, PC, src, dst, \
                                        SU, FF, temperature, daylight, humidity, \
                                        rainDesc, rainfall, windspeed, holiday, area, JF)

                                # if LI=="504-01335":
                                #     print(row)

                                rows.append(row)
                storeData()
            except Exception as e:
                print("Field access error in traffic json!")
                with open("error.log.txt", "a") as error:
                    s = "[%s] %s\n" % (datetime.now(), e)
                    error.write(s)
                
                fname = str(datetime.now()) + ".traffic.txt"
                with open(fname, "w") as jsonFile:
                    jsonFile.write(r.text)

def storeData():
    ## SEND to database service
    url = "http://database-service:8000/store"
    data = pickle.dumps(rows)
    r = requests.post(url,data=data)

collectData()