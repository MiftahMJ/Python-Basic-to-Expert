import os
import requests
from google.oauth2.service_account import Credentials
from googleapiclient.discovery import build
from twilio.rest import Client
import sendgrid
from sendgrid.helpers.mail import Mail, Email, To, Content
from pprint import pprint

# Amadeus API credentials from environment variables
API_KEY = os.getenv('AMADEUS_API_KEY')
API_SECRET = os.getenv('AMADEUS_API_SECRET')

# Google Sheets setup
SCOPES = ['https://www.googleapis.com/auth/spreadsheets']
SPREADSHEET_ID = os.getenv('GOOGLE_SHEET_ID')
SHEET2_RANGE = 'sheet2!A2:C2'  # To update 'sheet2' with name and email
PRICES_SHEET_RANGE = 'prices!A2:C'  # To append flight data to 'prices'

# Twilio credentials from environment variables
TWILIO_ACCOUNT_SID = os.getenv('TWILIO_ACCOUNT_SID')
TWILIO_AUTH_TOKEN = os.getenv('TWILIO_AUTH_TOKEN')
TWILIO_PHONE_NUMBER = os.getenv('TWILIO_PHONE_NUMBER')
YOUR_PHONE_NUMBER = os.getenv('YOUR_PHONE_NUMBER')

# SendGrid credentials from environment variables
SENDGRID_API_KEY = os.getenv('SENDGRID_API_KEY')
FROM_EMAIL = os.getenv('FROM_EMAIL')
TO_EMAIL = os.getenv('TO_EMAIL')

# FlightData class definition
class FlightData:
    def __init__(self, origin_city, origin_airport, destination_city, destination_airport, out_date, return_date,
                 stop_overs=0, via_city=""):
        self.origin_city = origin_city
        self.origin_airport = origin_airport
        self.destination_city = destination_city
        self.destination_airport = destination_airport
        self.out_date = out_date
        self.return_date = return_date
        self.stop_overs = stop_overs
        self.via_city = via_city

# Function to authenticate and access Google Sheets
def authenticate_google_sheets():
    creds = Credentials.from_service_account_file('credentials.json', scopes=SCOPES)
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
    try:
        response = requests.get(url, headers=headers, params=params)
        response.raise_for_status()  # Raise an exception for HTTP errors
        return response.json()
    except requests.RequestException as e:
        print(f"Error fetching flight data: {e}")
        return {'data': []}

# Function to append data to Google Sheets
def append_to_google_sheets(service, values, range_name):
    sheet = service.spreadsheets()
    body = {'values': values}
    try:
        result = sheet.values().append(
            spreadsheetId=SPREADSHEET_ID,
            range=range_name,
            valueInputOption='RAW',
            insertDataOption='INSERT_ROWS',
            body=body
        ).execute()
        print(f"{result.get('updates').get('updatedCells')} cells updated.")
    except Exception as e:
        print(f"Error appending to Google Sheets: {e}")

# Function to send SMS alert using Twilio
def send_sms_alert(message):
    client = Client(TWILIO_ACCOUNT_SID, TWILIO_AUTH_TOKEN)
    try:
        client.messages.create(
            body=message,
            from_=TWILIO_PHONE_NUMBER,
            to=YOUR_PHONE_NUMBER
        )
        print(f"SMS sent: {message}")
    except Exception as e:
        print(f"Error sending SMS: {e}")

# Function to send email alert using SendGrid
def send_email_alert(message):
    sg = sendgrid.SendGridAPIClient(api_key=SENDGRID_API_KEY)
    from_email = Email(FROM_EMAIL)
    to_email = To(TO_EMAIL)
    subject = "Flight Price Alert"
    content = Content("text/plain", message)
    mail = Mail(from_email, to_email, subject, content)
    try:
        response = sg.send(mail)
        print("Email sent:")
        print("Status Code:", response.status_code)
        print("Response Body:", response.body.decode())
        print("Response Headers:", response.headers)
    except Exception as e:
        print(f"Error sending email: {e}")

def main():
    # Collect user data
    first_name = input("Enter your first name: ")
    last_name = input("Enter your last name: ")
    email = input("Enter your email: ")

    # Prepare data for Google Sheets
    user_data = [[first_name, last_name, email]]

    # Google Sheets authentication
    service = authenticate_google_sheets()

    # Update user data in 'sheet2'
    append_to_google_sheets(service, user_data, SHEET2_RANGE)

    # Obtain access token for Amadeus API
    access_token = get_amadeus_access_token()

    # Example flight search parameters
    origin = 'JFK'
    destination = 'LAX'
    departure_date = '2024-08-15'

    # Fetch flight data
    flight_data = fetch_flight_data(access_token, origin, destination, departure_date)

    # Prepare flight data for Google Sheets
    flight_values = []
    for offer in flight_data.get('data', []):
        try:
            # Extract IATA code, price, and city
            itineraries = offer.get('itineraries', [])
            if not itineraries:
                print("No itineraries available")
                continue

            # Check for direct flights first
            direct = itineraries[0]['segments'][0]['arrival']['iataCode']
            price_info = offer.get('price', {})
            price = price_info.get('total', 'N/A')

            if price != 'N/A':
                price = float(price)
            else:
                price = 'N/A'

            # Append flight data
            flight_values.append([direct, 'N/A', price])

            # Send alerts if price is below a certain threshold
            if isinstance(price, float) and price < 200:
                message = f"Price alert! The price for a flight to {direct} is now ${price}."
                send_sms_alert(message)
                send_email_alert(message)

        except (KeyError, ValueError) as e:
            print(f"Skipping invalid data: {e}")
            flight_values.append(['N/A', 'N/A', 'N/A'])

    if flight_values:
        append_to_google_sheets(service, flight_values, PRICES_SHEET_RANGE)  # Update 'prices' sheet
    else:
        print("No flight data to append.")

    # Add specific data to the 'prices' sheet
    specific_data = [['Bali', 'DPS', 501]]
    append_to_google_sheets(service, specific_data, PRICES_SHEET_RANGE)

    # Check for flights with stopovers if no direct flights are found
    if not flight_values:
        print("No direct flights found, checking for flights with stopovers...")
        stopover_data = fetch_flight_data(access_token, origin, destination, departure_date)
        pprint(stopover_data)

        for offer in stopover_data.get('data', []):
            try:
                itineraries = offer.get('itineraries', [])
                if itineraries and len(itineraries[0]['segments']) > 1:
                    # Assume first segment is the origin to stopover, and second segment is stopover to destination
                    stopover_city = itineraries[0]['segments'][1]['arrival']['iataCode']
                    stopover_price_info = offer.get('price', {})
                    stopover_price = stopover_price_info.get('total', 'N/A')

                    if stopover_price != 'N/A':
                        stopover_price = float(stopover_price)
                    else:
                        stopover_price = 'N/A'

                    # Create a FlightData object with stopover info
                    flight_data = FlightData(
                        origin_city='New York',  # Example origin city
                        origin_airport=origin,
                        destination_city='Los Angeles',  # Example destination city
                        destination_airport=destination,
                        out_date=departure_date,
                        return_date='',  # Adjust as needed
                        stop_overs=1,
                        via_city=stopover_city
                    )

                    message = (f"Price alert! The price for a flight to {flight_data.destination_city} "
                               f"({flight_data.destination_airport}) with {flight_data.stop_overs} stopover(s) "
                               f"via {flight_data.via_city} is now ${stopover_price}.")
                    send_sms_alert(message)
                    send_email_alert(message)

            except (KeyError, ValueError) as e:
                print(f"Skipping invalid stopover data: {e}")

if __name__ == "__main__":
    main()
