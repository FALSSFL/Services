from datetime import datetime
import time

import os
import string
import ssl
import smtplib
from email.message import EmailMessage
from pymongo import MongoClient

CONNECTION_STRING = "mongodb+srv://contact:20Hyperlink21!@userlogin.xoq2kfh.mongodb.net/?retryWrites=true&w=majority&appName=UserLogin"




def sendEmail(collection):
    print("sending email :) ....")

    patients = test_collection.find({"followUp": False})

    # Iterate over the cursor to print each document
    for patient in patients:
        test_collection.update_one({"_id": patient['_id']}, {"$set": {"followUp": True}})       
        try :
            time.sleep(6)
            email_sender = 'Foot Ankle & Leg Specialists of South Florida'
            email_password = 'eovn iomj eipw ghfg'
            email_receiver = patient['email']

            subject = 'Follow-up: ' + (patient['firstName']).title()
            body = "Hi " + (patient['firstName']).title() + ", " +"\n\nWe hope this message finds you well! We wanted to reach out and see how you were feeling after your visit to our office. We'd like to know if we were able adequately assist in remedying your concerns and are steadily feeling better. If you have any questions or concerns, please call or email us! \n\nThank you so much for visiting us. Your visit is truly appreciated. \n\nPatient Support\nFoot, Ankle, & Leg Specialists of South Florida\n\nWeston (954) 389-5900      |  Email: contact@browardfootankleandlegspecialists.com\nPlantation (954) 720-1530  |  Website: www.browardfootankleandlegspecialists.com"


                
            em = EmailMessage()
            em['From'] = email_sender
            em['To'] = email_receiver
            em['Subject'] = subject
            em.set_content(body)

            context = ssl.create_default_context()

            with smtplib.SMTP('smtp.gmail.com', 587) as smtp:
                smtp.ehlo()
                smtp.starttls()
                smtp.ehlo()
                smtp.login('contact@browardfootankleandlegspecialists.com', email_password)
                smtp.sendmail(email_sender, email_receiver, em.as_string())
            print("email sent: " + email_receiver)
        except Exception as e:
            print(repr(e))
            continue
            
try:
    client = MongoClient(CONNECTION_STRING, 27017)

    db = client.get_database("test")

    test_collection = db.get_collection("patients")

except Exception as e:
    print(repr(e), "error occured")
    pass  
sendEmail(test_collection)

