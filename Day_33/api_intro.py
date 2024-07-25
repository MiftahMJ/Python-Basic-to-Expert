import requests
from datetime import datetime
my_lat=51.507351
my_lng=-0.127758

# response = requests.get(url="http://api.open-notify.org/iss-now.json")
# response.raise_for_status()
# data=response.json()
#
# longitude=data["iss position"]["longitude"]
# latitude=data["iss position"]["latitude"]
# print(data)

parameters = {
    "lat": my_lat,
    "lng": my_lng,
    "formaatted": 0,

}

def is_iss_overhead():
    response = requests.get("http://api.sunrise-sunset.org/json", params=parameters)
    response.raise_for_status()
    data = response.json()
    iss_latitude = float(data["iss_position"]["latitude"])
    iss_longitude = float(data["iss_position"]["longitude"])

    if my_lat - 5 <= iss_latitude <= my_lat + 5 and my_lng - 5 <= iss_longitude <= my_lng + 5:
        return True

def is_night():
    parameters = {
        "lat": my_lat,
        "lng": my_lng,
        "formaatted": 0,

    }
    response = requests.get("http://api.sunrise-sunset.org/json", params=parameters)
    response.raise_for_status()
    data = response.json()
    sunrise=int(data["results"]["sunrise"].split("T")[1].split(":")[0])
    sunset=int(data["results"]["sunset"].split("T")[1].split(":")[0])




    time_now=datetime.now().hour
    print(time_now.hour)
    if time_now>=sunset or time_now<= sunrise:
        return True

