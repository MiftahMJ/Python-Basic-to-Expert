# class DataManager:
#     #This class is responsible for talking to the Google Sheet.
#     pass
#
# CLIENT_ID="292997109938-qlfg5o3u3sk0feq1eq3idr4arvos55k7.apps.googleusercontent.com"
# CLIENT_SECRET="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"


# using SendGrid's Python Library
# https://github.com/sendgrid/sendgrid-python
# import os
# from sendgrid import SendGridAPIClient
# from sendgrid.helpers.mail import Mail
#
# message = Mail(
#     from_email='miftahjabeen.com',
#     to_emails='avengerpak77.com',
#     subject='Sending with Twilio SendGrid is Fun',
#     html_content='<strong>and easy to do anywhere, even with Python</strong>')
# try:
#     sg = SendGridAPIClient(os.environ.get('SENDGRID_API_KEY'))
#     response = sg.send(message)
#     print(response.status_code)
#     print(response.body)
#     print(response.headers)
# except Exception as e:
#     print(e.message)
import sendgrid
from sendgrid.helpers.mail import Mail, Email, To, Content

# Set up SendGrid client with your API key
sg = sendgrid.SendGridAPIClient(api_key='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')

# Create email content
from_email = Email("miftahjabeen@gmail.com")
to_email = To("avengerpak77@gmail.com")
subject = "Flight Booking Confirmation"
content = Content("text/plain", "Your flight booking has been confirmed!")

# Create Mail object with 'personalizations' and 'content'
mail = Mail(from_email, to_email, subject, content)

# Send email
try:
    response = sg.send(mail)
    print("Status Code:", response.status_code)
    print("Response Body:", response.body)
    print("Response Headers:", response.headers)
except Exception as e:
    print("An error occurred:", str(e))

