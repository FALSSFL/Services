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

    patients = test_collection.find({"review": False})

    # Iterate over the cursor to print each document
    for patient in patients:
        test_collection.update_one({"_id": patient['_id']}, {"$set": {"review": True}})       
        try :
            time.sleep(50)
            email_sender = 'Foot Ankle & Leg Specialists of South Florida'
            email_password = 'eovn iomj eipw ghfg'
            email_receiver = patient['email']

            subject = 'We\'d love to hear your feedback, ' + (patient['firstName']).title() +  ' !'
            body = "Dear " + (patient['firstName']).title() + ", " +"\n\nI hope this message finds you well! I wanted to reach out and ask if you could take a moment to share your experience with our team at Foot Ankle & Leg Specialists of South Florida using this link:\n\nWeston Office:\nhttps://g.page/r/CeogA8kzWS1SEBM/review.\n\nPlantation Office:\nhttps://g.page/r/CRzsM2QSDKhHEBM/review \n\nYour feedback means a lot to us, and it would be incredibly helpful for others who are considering us. \n\nWhether it's a quick rating or a detailed review, your honest opinion will provide valuable insights to others. Plus, it's a great way to support us! \n\nThank you so much for considering this request. Your support is truly appreciated. \n\nPatient Support\nFoot, Ankle, & Leg Specialists of South Florida\n\nWeston (954) 389-5900      |  Email: contact@browardfootankleandlegspecialists.com\nPlantation (954) 720-1530  |  Website: www.browardfootankleandlegspecialists.com"


                
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

