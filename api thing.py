import requests
import json
import time
import serial

time.sleep(3)
arduino = serial.Serial(port='COM17', baudrate=9600, timeout=.1)
username = arduino.readline().decode("utf-8")
while username == "":
    print(arduino.readline().decode("utf-8"))
    username = arduino.readline().decode("utf-8")
    time.sleep(0.05)
username = username.strip()
print("got it", username)

# username = input("Username please: ")
response = requests.get(f"https://api.jikan.moe/v4/users/{username}/history")
print(response)

lenarr = []
ids = []
timearr = []
hrPrEp = 0
minPrEp = 0


try:
    for i in range(len(response.json()['data'])):   # get data in .json format
        if response.json()['data'][i-1]['entry']['type'] == "anime":    # entry has to be anime not manga
            lenarr.append(json.dumps(response.json()['data'][i-1]['entry']['type'], indent=4))
            ids.append(json.dumps(response.json()['data'][i-1]['entry']['mal_id'], indent=4))   # ids of animes in history
except:
    print("please try again")
    exit()

print(len(lenarr))
ids.sort()
print(ids)
iddict = {i:ids.count(i) for i in ids}  # counts duplicate ids
print(iddict)
keys = list(iddict.keys())
for i in range(len(iddict)):
    response = requests.get(f"https://api.jikan.moe/v4/anime/{keys[i-1]}")  # get duration of each entry
    print(keys[i-1], iddict[keys[i-1]], "*",  response.json()['data']['duration'])
    # minutes duration of entry
    if "min" in response.json()['data']['duration']:
        minIndex = response.json()['data']['duration'].index("min")
        if minIndex >= 3:
            minPrEp = int(response.json()['data']['duration'][minIndex - 3] + response.json()['data']['duration'][minIndex - 2])    # if entry is a movie with minutes
        elif minIndex == 2:
            minPrEp = int(response.json()['data']['duration'][minIndex - 2])    # else
        timearr.append(int(iddict[keys[i-1]]) * minPrEp)
    else:
        minPrEp = 0 # if entry is a movie without minutes
    print(int(iddict[keys[i-1]]) * minPrEp)
    # hours
    if "hr" in response.json()['data']['duration']:
        hrIndex = response.json()['data']['duration'].index("hr")
        hrPrEp = int(response.json()['data']['duration'][hrIndex - 2]) * 60
        timearr.append(int(iddict[keys[i-1]]) * hrPrEp)
    else:
        hrPrEp = 0  # if no hours
    print(iddict[keys[i-1]] * hrPrEp)
    time.sleep(1)
print(timearr)
print(sum(timearr), "minutes of watchtime in the past 3 weeks")
print(round(sum(timearr) / 60, 3), "hours of watchtime in the past 3 weeks")
print("thats", round((sum(timearr)/(3*7*24*60))*100, 2), "\b% of each day")