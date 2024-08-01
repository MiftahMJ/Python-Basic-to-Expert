# class FlightData:
#     #This class is responsible for structuring the flight data.
#     pass
# # sms
#
# API_KEY="8d94994696df65fff3a87ffc199992c5-380d9fcb-3ccf-49da-a8b8-f45f11d7dc96"

from twilio.rest import Client

account_sid = 'AC20d12d60bdf2802b0d4eb2ff23eb9684'
auth_token = '8473e5f73595ee67e9378ff06689b046'
client = Client(account_sid, auth_token)

message = client.messages.create(
    body="This is miftah jabeen",
  from_='+18145243904',
  to='+9203156867866'
)

print(message.body)