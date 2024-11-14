from striprtf.striprtf import rtf_to_text
import os
import openpyxl
import string
import datetime
import ssl
import smtplib
from email.message import EmailMessage
from email.mime.text import MIMEText
import traceback
import time
from pymongo import MongoClient
import pandas as pd

path = "/home/contact/tools/officeTools/emailTool/scripts/sendEmails/doctorNotes/logs"
path2 = "/home/contact/tools/officeTools/emailTool/scripts/sendEmails/doctorNotes/downloads"
os.chdir(path2)


def readFiles(num, fileName, outputFile, file_path, path):
    try:
        with open(file_path, 'r') as file:
            content = file.read()
            text = rtf_to_text(content)

        textToReplace = "Thank you for visiting our office. We appreciate the opportunity to see you and we will always do everything possible to educate you and to get you well."
        replacingText = "Thank you for visiting our office. We appreciate the opportunity to see you and we will always do everything possible to educate you and to get you well. We value your opinion and take great strides to make your experience a good one.  \n\nPlease take a moment when you have an opportunity and fill out a survey about me, my office and staff and the care you received by visiting www.healthgrades.com/review/X7K6G. Thank you!"
    

        res = list(text)


        i = 0
        j = i + 1

        while res[j] != "#":
            j += 1
        res[i : j + 1] = ""
        j = i + 1

        patientNumber = ''.join(res[i:i + 6])

        patientName = ""

        for k in range(i, 100):
            if ''.join(res[i:j]) == "Dear":
                i,j = j, j + 1
                while res[j] != ',':
                    patientName += res[j]
                    j += 1
                break
            elif len(''.join(res[i:j + 1])) == 10:
                # print("hi")
                i += 1
                j = i + 1
            j += 1
        i = i + len(patientName)
        # print(patientName)

        for k in range(i, len(res)):
            # print(''.join(res[i:j]))
            if ''.join(res[i:j]) == "Thank you":
                j = i + 1
                # print("exited")
                break
            elif len(''.join(res[i:j + 1])) == len("Thank you") and ''.join(res[i:j + 1]) != "Thank you":
                i += 1
                # print("sup")
                j = i + 1
            j += 1

        # print(i)

        res[i : i + len(textToReplace)] = ""
        res.insert(i, replacingText)

        i = len(res) // 2
        j = i + 1
        start = i

        for k in range(start, len(res)):
            stringMatch = ''.join(res[i:j])
            if stringMatch.lstrip() == ("We value"):
                res[i:len(res) - 1] = ""
                break
            elif (len(stringMatch.lstrip()) > (len("We value"))) and (stringMatch.lstrip() != "We value"):
                i = j
            j += 1

        outputFile.write(("---------------" + "\n"))
        outputFile.write((str(num) + "\n"))
        outputFile.write(("---------------" + "\n"))
        outputFile.write((str(patientName) + "\n"))
        outputFile.write(("---------------" + "\n"))
        outputFile.write((str(patientNumber) + "\n"))
        outputFile.write(("---------------" + "\n"))
        outputFile.write((str(fileName) + '\n'))
        outputFile.write(("---------------" + "\n"))
        outputFile.write((str(patientName) + ": Personal Request from Dr. Carlo Messina\n"))
        outputFile.write(("---------------" + "\n"))
        outputFile.write((''.join(res)))




        patientName = patientName.split(' ', 1)[0]


        os.chdir(path)

        # print("looking through DB to find patients' emails.....")
        patient =  test_collection.find_one({"id": patientNumber})  

        if (patient):

                   
            res[0 : 7] = ""
            abc = ''.join(res)
           
            os.remove(file_path)

            
            email_sender = 'contact@browardfootankleandlegspecialists.com'
            email_password = 'eovn iomj eipw ghfg'
            email_receiver = patient['email']

            subject = (patient['firstName']).title() + ": Personal Request from Dr. Carlo Messina\n"
            body = str(abc) +  """

            Weston (954) 389-5900      |  Email: contact@browardfootankleandlegspecialists.com
            Plantation (954) 720-1530  |  Website: www.browardfootankleandlegspecialists.com


            """
            em = EmailMessage()
            em = MIMEText(body)
            em['From'] = email_sender
            em['To'] = email_receiver
            em['Subject'] = subject
            em.add_header('Content-Type', 'text')
            
            
            context = ssl.create_default_context()
            print("sending email.....")
            with smtplib.SMTP('smtp.gmail.com', 587) as smtp:
               smtp.ehlo()
               smtp.starttls()
               smtp.ehlo()
               smtp.login(email_sender, email_password)
               smtp.sendmail(email_sender, email_receiver, em.as_string())
               print("email sent: ",  email_receiver)
        
            time.sleep(30)
            
            return [fileName, int(patientNumber), patientName]
              
    except Exception:
        traceback.print_exc()
        pass
            

os.chdir(path2)
for file in os.listdir():
# Check whether file is in text format or not
   if file.endswith(".csv"):
       file_name = file
       print(file_name)
       read_file = pd.read_csv(file_name)
       read_file.to_excel('output.xlsx', index=None, header=True)
       file_name = "output.xlsx"

print(file_name)



os.chdir(path2)
wb2 = openpyxl.load_workbook(file_name)


ws2 = wb2.active




CONNECTION_STRING = "mongodb+srv://contact:20Hyperlink21!@userlogin.xoq2kfh.mongodb.net/?retryWrites=true&w=majority&appName=UserLogin"
try:
    # Create a connection using MongoClient
    client = MongoClient(CONNECTION_STRING, 27017)

    # Access the 'UserLogin' database
    db = client.get_database("test")

    # print(client.list_database_names())

    # Access the 'test' collection
    test_collection = db.get_collection("patients")
    # users = test_collection.get_collection("users")
    # Get the documents from the collection
    """
    for patient in test_collection.find():
        print(patient)
    """
    # test_collection.insert_one({"hello world": "hi"})

except Exception as e:
    print("An error occurred:", e)

for row in ws2.iter_rows(values_only=True):
    data = {"email": row[0], "lastName": row[1], "firstName": row[2], "id": row[3], "review": False}
    existingUser = test_collection.find_one({"id": row[3]})
    if not existingUser:
        test_collection.insert_one(data)


   
allData = []
num = 0

os.chdir(path)

if os.path.exists("emails.txt"):
  os.remove("emails.txt")
else:
  createFile = open("emails.txt", "x")

outputFile = open("emails.txt", "a")

os.chdir(path2)

print("looking through DB to find patients' emails.....")
for file in os.listdir():
    # Check whether file is in text format or not
    if file.endswith(".rtf"):
        file_path = f"{path2}/{file}"
        num += 1
  
        # call read text file function
        allData.append(readFiles(num, file, outputFile, file_path, path))


