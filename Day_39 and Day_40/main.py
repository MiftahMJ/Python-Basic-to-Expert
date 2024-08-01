import requests
from google.oauth2.service_account import Credentials
from googleapiclient.discovery import build
from twilio.rest import Client

# Amadeus API credentials
API_KEY = "5RXbh2fsEtLmjl5zobpbN6SGSteBUcMj"
API_SECRET = "4FCR4tMlE9CciA7h"

# Google Sheets setup
SCOPES = ['https://www.googleapis.com/auth/spreadsheets']
SPREADSHEET_ID = '1nPE2qzdCYREByNMtZvBqQFk7rEA_5_uZkoUXIFidA6s'
RANGE_NAME = 'prices!A2:C2'

# Twilio credentials
TWILIO_ACCOUNT_SID = 'AC20d12d60bdf2802b0d4eb2ff23eb9684'
TWILIO_AUTH_TOKEN = '8473e5f73595ee67e9378ff06689b046'
TWILIO_PHONE_NUMBER = '+18145243904'
YOUR_PHONE_NUMBER = '+9203156867866'

# Function to authenticate and access Google Sheets
def authenticate_google_sheets():
    creds = Credentials.from_service_account_file('credentials .json', scopes=SCOPES)
    service = build('sheets', 'v4', credentials=creds)
    return service

# Function to authenticate with Amadeus API and get an access token
def get_amadeus_access_token():
    url = "https://test.api.amadeus.com/v1/security/oauth2/token"
    headers = {
        'Content-Type': 'application/x-www-form-urlencoded'
    }
    data = {
        'grant_type': 'client_credentials',
        'client_id': API_KEY,
        'client_secret': API_SECRET
    }
    response = requests.post(url, headers=headers, data=data)
    token = response.json().get('access_token')
    return token

# Function to fetch flight data using Amadeus API
def fetch_flight_data(access_token, origin, destination, departure_date):
    url = "https://test.api.amadeus.com/v2/shopping/flight-offers"
    headers = {
        'Authorization': f'Bearer {access_token}'
    }
    params = {
        'originLocationCode': origin,
        'destinationLocationCode': destination,
        'departureDate': departure_date,
        'adults': 1,
        'max': 5
    }
    response = requests.get(url, headers=headers, params=params)
    return response.json()

# Function to append data to Google Sheets
def append_to_google_sheets(service, values):
    sheet = service.spreadsheets()
    body = {'values': values}
    try:
        result = sheet.values().append(
            spreadsheetId=SPREADSHEET_ID,
            range=RANGE_NAME,
            valueInputOption='RAW',
            insertDataOption='INSERT_ROWS',
            body=body
        ).execute()
        print(f"{result.get('updates').get('updatedCells')} cells updated.")
    except Exception as e:
        print(f"Error appending to Google Sheets: {e}")

# Function to send SMS alert using Twilio
def send_sms_alert(city_name, iata_code, price):
    client = Client(TWILIO_ACCOUNT_SID, TWILIO_AUTH_TOKEN)
    message = f"Price alert! The price for a flight to {city_name} ({iata_code}) is now ${price}."
    try:
        client.messages.create(
            body=message,
            from_=TWILIO_PHONE_NUMBER,
            to=YOUR_PHONE_NUMBER
        )
        print(f"SMS sent: {message}")
    except Exception as e:
        print(f"Error sending SMS: {e}")

def main():
    # Google Sheets authentication
    service = authenticate_google_sheets()

    # Obtain access token for Amadeus API
    access_token = get_amadeus_access_token()

    # Example flight search parameters
    origin = 'JFK'
    destination = 'LAX'
    departure_date = '2024-08-15'

    # Fetch flight data
    flight_data = fetch_flight_data(access_token, origin, destination, departure_date)

    # Prepare data for Google Sheets
    values = []
    for offer in flight_data.get('data', []):
        try:
            # Extract IATA code, price, and city
            iata_code = offer['itineraries'][0]['segments'][0]['arrival']['iataCode']
            price_info = offer.get('price', {})
            price = price_info.get('total', 'N/A')

            # Convert price to float if it's a valid number
            if price != 'N/A':
                price = float(price)
            else:
                price = 'N/A'

            # Determine city name
            city_name = iata_code  # Use IATA code for city name in this example

            # Append data
            values.append([city_name, iata_code, price])

            # Send SMS alert if price is below a certain threshold
            if isinstance(price, float) and price < 200:  # Set your desired price threshold
                send_sms_alert(city_name, iata_code, price)
        except (KeyError, ValueError) as e:
            print(f"Skipping invalid data: {e}")
            values.append(['N/A', 'N/A', 'N/A'])

    if values:
        append_to_google_sheets(service, values)
    else:
        print("No flight data to append.")

if __name__ == "__main__":
    main()
