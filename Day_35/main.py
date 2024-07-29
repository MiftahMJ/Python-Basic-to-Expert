import params
import requests
OMW_Endpoint="https://api.openweathermap.org/data/2.5/onecall"
API="07a5eaf65cfeb9c48c28da5ae573e4e6"

weather_params ={

    "lat":51.507351,
        "lon":-0.127758,
"appid":API,
}

response=requests.get(OMW_Endpoint, params= weather_params)
print(response.json())