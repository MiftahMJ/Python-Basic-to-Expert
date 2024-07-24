# import smtplib
#
#
# my_email="abc@gmail.com"
# password="124."
# with smtplib.SMTP("smtp.gmail.com") as connection:
#     connection.starttls()
#     connection.login(user=my_email, password=password)
#     connection.sendmail(from_addr=my_email, to_addrs="xyz @gmail.com", msg="Subject: Hello\n\nThis is the body of my email")
#     connection.close()
# import datetime as dt
# now=dt.datetime.now()
# year=now.year
# month=now.month
# day_of_week=now.weekday()
# print(day_of_week)
#
# date_of_birth=dt.datetime(year=2001,month=5,day=28)
# print(date_of_birth)
# import random
# import smtplib
# import datetime as dt
#
# my_email="abc@gmail.com"
# my_pswd="pa6."
#
# now=dt.datetime.now()
# weekday=now.weekday()
# if weekday==3:
#     with open("quotes.txt") as quote:
#         all_quotes=quote.readlines()
#         quote=random.choice(all_quotes)
#     print(quote)
#     with smtplib.SMTP("smtp.gmail.com") as connection:
#         connection.starttls()
#         connection.login(my_email,my_pswd)
#         connection.sendmail(from_addr=my_email, to_addrs=my_email,msg=f"Subject: Monday Motivation\n\n{quote}")
import random
import smtplib
from datetime import datetime
import pandas
today=datetime.now()
today_tiple=(today.month,today.day)
data=pandas.read_csv("birthday.csv")

my_email="abc@gmail.com"
my_pswd="pa6."

birthday_dict={(data_row["month"],data_row["day"]):data_row for (index,data_row) in data.iterrows()}

if today_tiple in birthday_dict:
    birthday_person=birthday_dict[today_tiple]
    file_path=f"letter_template/letter_{random.randint(1,3)}.txt"
    with open(file_path) as letter_file:
        contents=letter_file.read()
        contents=contents.replace(["Name"],birthday_person["name"])

    with smtplib.SMTP("smtp.gmail.com") as connection:
        connection.starttls(
        connection.login(my_email,my_pswd)

        connection.sendmail(from_addr=my_email,to_addrs=["email"],
                                msg=f"Subject: Happy Birthday\n\n{contents}"

        )

