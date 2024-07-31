import requests
from datetime import datetime
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request
from googleapiclient.discovery import build
import os
import pickle

# Nutritionix API credentials
APP_ID = "a51702f5"
API_KEY = "12702c9a5ea7bf901324a76abec019bf"

# User details for the exercise query
GENDER = "female"
WEIGHT_KG = "55"
HEIGHT_CM = "153"
AGE = "23"

# Endpoints and authentication
exercise_endpoint = "https://trackapi.nutritionix.com/v2/natural/exercise"
SCOPES = ['https://www.googleapis.com/auth/spreadsheets']


# Function to authenticate Google Sheets API
def authenticate_google_sheets():
    creds = None
    if os.path.exists('token.pickle'):
        with open('token.pickle', 'rb') as token:
            creds = pickle.load(token)
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file('credentials.json', SCOPES)
            creds = flow.run_local_server(port=0)
        with open('token.pickle', 'wb') as token:
            pickle.dump(creds, token)
    return creds


# Function to append data to Google Sheets
# Function to append data to Google Sheets
def append_to_google_sheets(values):
    creds = authenticate_google_sheets()
    service = build('sheets', 'v4', credentials=creds)
    sheet = service.spreadsheets()

    # Use the correct spreadsheet ID and range name
    spreadsheet_id = '1q21zC_pz4Ay7GYiyiUrSNLN98_V2CzDi6FlmEG0g4_M'
    range_name = 'workouts!A2:E2'

    body = {'values': values}
    try:
        result = sheet.values().append(
            spreadsheetId=spreadsheet_id,
            range=range_name,
            valueInputOption='RAW',
            insertDataOption='INSERT_ROWS',
            body=body
        ).execute()
        print(f"{result.get('updates').get('updatedCells')} cells updated.")
    except Exception as e:
        print(f"Error appending to Google Sheets: {e}")

def main():
    # Get user input for exercises
    exercise_text = input("Tell me which exercises you did: ")

    headers = {
        'Content-Type': 'application/json',
        'x-app-id': APP_ID,
        'x-app-key': API_KEY
    }
    parameters = {
        "query": exercise_text,
        "gender": GENDER,
        "weight_kg": WEIGHT_KG,
        "height_cm": HEIGHT_CM,
        "age": AGE
    }

    # Make a request to Nutritionix API
    response = requests.post(exercise_endpoint, json=parameters, headers=headers)
    result = response.json()
    print(result)

    # Prepare data for Google Sheets
    today_date = datetime.now().strftime("%d/%m/%Y")
    now_time = datetime.now().strftime("%X")

    values = []
    for exercise in result.get("exercises", []):
        values.append([
            today_date, now_time, exercise["name"].title(), exercise["duration_min"], exercise["nf_calories"]
        ])

    if values:
        append_to_google_sheets(values)
    else:
        print("No exercises data to append.")


if __name__ == "__main__":
    main()
