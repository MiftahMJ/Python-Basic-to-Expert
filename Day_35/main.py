# import params
# import requests
#
# OMW_Endpoint = "https://api.openweathermap.org/data/2.5/onecall"
# api_key = "07a5eaf65cfeb9c48c28da5ae573e4e6"
#
# weather_params = {
#
#     "lat": 51.507351,
#     "lon": -0.127758,
#     "appid": api_key,
#     "exclude": ""
# }
#
# response = requests.get(OMW_Endpoint, params=weather_params)
# response.raise_for_status()
# weather_data = response.json()
# print(weather_data)
import requests
from twilio.rest import Client

OMW_Endpoint = "https://api.openweathermap.org/data/2.5/onecall"
api_key = "891444a2132c35643acaa1087087b6c6"  # Replace with your actual API key
account_sid = "ACfb67ae9fc94eb250fc5b354df4678d9f"
auth_token = "0d38303ea72eddb99889171f34f6098d"

weather_params = {
    "lat": 51.507351,
    "lon": -0.127758,
    "appid": api_key,
    "exclude": "minutely,hourly",  # Specify parts to exclude if needed
}

response = requests.get(OMW_Endpoint, params=weather_params)

try:
    response.raise_for_status()
    weather_data = response.json()
    print(weather_data)
except requests.exceptions.HTTPError as err:
    print(f"HTTP error occurred: {err}")
except Exception as err:
    print(f"Other error occurred: {err}")

client = Client(account_sid, auth_token)

message = client.messages.create(
    body="It's raining outside",
    from_='+12086035070',
    to='+9203156867866'
)

print(message.sid)
