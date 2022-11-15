import requests
import json
import time
import serial

# arduino = serial.Serial(port='COM4', baudrate=115200, timeout=.1)
# username = arduino.readline().decode("utf-8")

username = input("Username please: ")
response = requests.get(f"https://api.jikan.moe/v4/users/{username}/history")
print(response)

lenarr = []
ids = []
timearr = []
hrPrEp = 0
minPrEp = 0



for i in range(len(response.json()['data'])):
    if response.json()['data'][i-1]['entry']['type'] == "anime":
        lenarr.append(json.dumps(response.json()['data'][i-1]['entry']['type'], indent=4))
        ids.append(json.dumps(response.json()['data'][i-1]['entry']['mal_id'], indent=4))
print(len(lenarr))
ids.sort()
print(ids)
iddict = {i:ids.count(i) for i in ids}
print(iddict)
keys = list(iddict.keys())
for i in range(len(iddict)):
    response = requests.get(f"https://api.jikan.moe/v4/anime/{keys[i-1]}")
    print(keys[i-1], iddict[keys[i-1]], "*",  response.json()['data']['duration'])
    # minutes
    if "min" in response.json()['data']['duration']:
        minIndex = response.json()['data']['duration'].index("min")
        if minIndex >= 3:
            minPrEp = int(response.json()['data']['duration'][minIndex - 3] + response.json()['data']['duration'][minIndex - 2])
        elif minIndex == 2:
            minPrEp = int(response.json()['data']['duration'][minIndex - 2])
        timearr.append(int(iddict[keys[i-1]]) * minPrEp)
    else:
        minPrEp = 0
    print(int(iddict[keys[i-1]]) * minPrEp)
    # hours
    if "hr" in response.json()['data']['duration']:
        hrIndex = response.json()['data']['duration'].index("hr")
        hrPrEp = int(response.json()['data']['duration'][hrIndex - 2]) * 60
        timearr.append(int(iddict[keys[i-1]]) * hrPrEp)
    else:
        hrPrEp = 0
    print(iddict[keys[i-1]] * hrPrEp)
    time.sleep(1)
print(timearr)
print(sum(timearr), "minutes of watchtime in the past 3 weeks")
print(round(sum(timearr) / 60, 3), "hours of watchtime in the past 3 weeks")
print("thats", round((sum(timearr)/(3*7*24*60))*100, 2), "percent of each day")