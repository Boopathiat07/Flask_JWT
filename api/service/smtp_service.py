import os
from dotenv import load_dotenv
import smtplib, random

load_dotenv()

MAIL_USERNAME = os.getenv('MAIL_USERNAME')
MAIL_PASSWORD = os.getenv('MAIL_PASSWORD')

advertisement_list = [
    "Amazing deals on electronics! Don't miss out!",
    "Introducing our new product line - Check it out!",
    "Limited-time offer! Get discounts on selected items!",
    "Upgrade your wardrobe with our latest fashion collection!",
    "Special discounts for our loyal customers - Shop now!",
]

def generate_advertisement():
    return random.choice(advertisement_list)

def send_email(): 
    advertisement = generate_advertisement()
    server = smtplib.SMTP ('smtp.gmail.com', 587)
    server.starttls()
    server.login(MAIL_USERNAME, MAIL_PASSWORD)

    message = f'Subject: Advertisement\n\n{advertisement}'

    server.sendmail(MAIL_USERNAME, '20p209@kce.ac.in', message)
    server.quit()
