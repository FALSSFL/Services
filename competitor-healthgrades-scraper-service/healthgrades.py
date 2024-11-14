import requests
import json
import html_to_json
import csv
import os 

# path = "/Users/bryanserrano/Desktop/officeTools/"
# os.chdir(path)

import json
from collections import defaultdict

path = "/Users/bryanserrano/Desktop/officeTools/OfficeScripts"
os.chdir(path)

doctors = defaultdict(dict)
  
# Opening JSON file
f = open('messina.json')
  
# returns JSON object as 
# a dictionary
doctors['messina'] = json.load(f)
f.close()

f = open('sansone.json')
doctors['sansone'] = json.load(f)
f.close()

f = open('kazamias.json')
doctors['kazamias'] = json.load(f)
f.close()

f = open('wagner.json')
doctors['wagner'] = json.load(f)
f.close()  

f = open('dorfman.json')
doctors['dorfman'] = json.load(f)
f.close()  
# Closing file


if os.path.exists("reviews.csv"):
  os.remove("reviews.csv")
else:
  createFile = open("reviews.csv", "x")

with open('reviews.csv', 'w', newline='') as file:
     writer = csv.writer(file)
     for key in doctors:
        writer.writerow(["Doctor Name: ", doctors[key]['providerName']])
        writer.writerow(["Doctor Healtgrades URL: ", doctors[key]['providerUrl']])
        writer.writerow(["Doctor City: ", doctors[key]['locationCity']])
        writer.writerow(["Response Count", "Review Count", "Actual Score", "Rounded Score"])
        writer.writerow([str(doctors[key]['model']['overall']['responseCount']), str(doctors[key]['model']['overall']['reviewCount']), str(doctors[key]['model']['overall']['actualScore']), str(doctors[key]['model']['overall']['roundedScore'])])

        writer.writerow(["Rating", "Patient Name", "Date", "Review"])

        for j in range(len(doctors[key]['results'])):
          writer.writerow([str(doctors[key]['results'][j]['overallScore']), str(doctors[key]['results'][j]['displayName']), str(doctors[key]['results'][j]['submittedDate']), str(doctors[key]['results'][j]['commentText'])])

        writer.writerow(["-------------------"])

# top 5 competitor doctors 
# read all the data and load them seperately, then merge to one dictionary, dictionary of dictionaries, then write to excel. manually create tables