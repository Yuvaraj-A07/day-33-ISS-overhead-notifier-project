import time
import manager as mg
import requests
from datetime import datetime
import smtplib

MY_LAT = mg.MY_LAT
MY_LONG = mg.MY_LONG

my_mail = mg.my_mail
password = mg.password


def up():
    response = requests.get(url="http://api.open-notify.org/iss-now.json")
    response.raise_for_status()
    data = response.json()

    iss_latitude = float(data["iss_position"]["latitude"])
    iss_longitude = float(data["iss_position"]["longitude"])

    # Your position is within +5 or -5 degrees of the ISS position.
    if (MY_LAT - 5 <= iss_latitude <= MY_LAT + 5) and (MY_LONG - 5 <= iss_longitude <= MY_LONG + 5):
        return True


def is_night():
    parameters = {
        "lat": MY_LAT,
        "lng": MY_LONG,
        "formatted": 0,
    }

    response = requests.get("https://api.sunrise-sunset.org/json", params=parameters)
    response.raise_for_status()
    data = response.json()
    sunrise = int(data["results"]["sunrise"].split("T")[1].split(":")[0])
    sunset = int(data["results"]["sunset"].split("T")[1].split(":")[0])

    time_now = datetime.now().hour
    if sunset <= time_now <= sunrise:
        return True


while True:
    time.sleep(60)
    if up() and is_night():
        with smtplib.SMTP("smtp.gmail.com") as send_quote:
            send_quote.starttls()
            send_quote.login(user=my_mail, password=password)
            send_quote.sendmail(from_addr=my_mail,
                                to_addrs=my_mail,
                                msg=f"Subject:Look up \n\nHey! look up ISS is above you in the sky.")

# BONUS: run the code every 60 seconds.
