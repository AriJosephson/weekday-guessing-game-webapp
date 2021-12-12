# -*- coding: utf-8 -*-
"""
Created on Mon Dec  6 22:39:59 2021

@author: Ari
"""
# For the main app
import datetime
import locale
import random
from flask import Flask, request, render_template, redirect

# For email feedback
import smtplib, ssl
import time
from email.mime.text import MIMEText
from email.mime.image import MIMEImage
from email.mime.multipart import MIMEMultipart
from os import getcwd

port = 465  # For SSL
smtp_server = "smtp.gmail.com"
sender_email = "fortestanddev@gmail.com"
receiver_email = "arij76257@gmail.com"
password = open(getcwd()+'youshallnot.txt','r').read()

message = MIMEMultipart("alternative")
message["Subject"] = "Feedback for Weekday Guessing Game"
message["From"] = sender_email
message["To"] = receiver_email

def generate_date(cutoff=80, lang='en_US', date_format='%Y-%m-%d'):
    locale.setlocale(locale.LC_ALL, lang+'.utf8') # need to add the suffix so it'll work on the server
    randunivar = random.uniform(0, 1) # get uniform random variable from 0 to 1
    
    if randunivar < cutoff/100: # cutoff% of the time do dates within a few centuries of the present
        start_date = datetime.date(1582, 10, 15)
        end_date = datetime.date(2400, 12, 31)

    else:
        start_date = datetime.date(1582, 10, 15)
        end_date = datetime.date(9999, 12, 31)
    
    time_between_dates = end_date - start_date
    days_between_dates = time_between_dates.days

    random_number_of_days = random.randrange(days_between_dates)
    random_date = start_date + datetime.timedelta(days=random_number_of_days)

    return random_date.strftime(date_format), random_date.strftime('%A')

app = Flask(__name__)

@app.route('/')
def my_form():
    return render_template("weekday_guesser.html", cutoff=80)

@app.route('/', methods=['POST'])
def generate_date_post():
    cutoff = int(request.form['cutoff'])
    language = request.form['language']
    date_format = request.form['date_format']

    this_date, weekday = generate_date(cutoff=cutoff,
                                       lang=language,
                                       date_format=date_format.replace('_',' '))
    
    return render_template("weekday_guesser.html", 
                           date=this_date, 
                           weekday=weekday)

@app.route('/feedback_post', methods=['POST'])
def feedback_post():
    text = request.form['feedback_text']
    part1 = MIMEText(text, "plain")
    message.attach(part1)
    context = ssl.create_default_context()
    with smtplib.SMTP_SSL(smtp_server, port, context=context) as server:
        server.login(sender_email, password)
        server.sendmail(sender_email, receiver_email, message.as_string())
    return redirect(request.referrer)

if __name__ == '__main__':
    app.run()