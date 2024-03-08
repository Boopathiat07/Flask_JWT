from flask import Blueprint
import os
from dotenv import load_dotenv
from flask_crontab import Crontab
from create_app import app
import smtplib


load_dotenv()

MAIL_USERNAME = os.getenv('MAIL_USERNAME')
MAIL_PASSWORD = os.getenv('MAIL_PASSWORD')


emailTask = Blueprint('emailTask', __name__)
crontab = Crontab(app)


# @emailTask.route("/sendEmail", methods = ['GET'])
@crontab.job(minute="1")
def send_email(): 
    print("Hello hi")
    server = smtplib.SMTP ('smtp.gmail.com', 587)
    server.starttls()
    server.login(MAIL_USERNAME, MAIL_PASSWORD)

    message = 'sending this from python!'
    server.sendmail(MAIL_USERNAME, '20p209@kce.ac.in', message)
    server.quit()

    # return jsonify({"message": "Message sent"})


