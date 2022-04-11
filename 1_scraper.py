# import libraries
# coding: utf-8
import urllib3
from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.common.exceptions import TimeoutException

from requests import Session

import json
import requests
from time import gmtime, strftime

import os
import json
import csv
from bs4 import BeautifulSoup

# Import unidecode module from unidecode
from unidecode import unidecode

sports = "OSKARAI"

DATA_PATH = "raw/"+sports+"/"
RESULTS_PATH = "logs/"+sports+"/"
TRACK_ENDED = True
odds = {}
finished = {}

def doesEventLogFileExist(event):
    return (getEventFileName(event) in os.listdir())

def getEventFileName(event):
    return str(event)+".csv"

def createNewEventLogFile(event):
    with open(RESULTS_PATH+getEventFileName(event['id']), 'w') as outcsv: # create this file
        writer = csv.writer(outcsv)
        writer.writerow(["Date", unidecode(event["teams"]["home"]), "X", unidecode(event["teams"]["away"]), event['date_start']])
        outcsv.close()
        
def createNewEventLogFile(name):
    with open(getEventFileName(name), 'w') as outcsv: # create this file
        writer = csv.writer(outcsv)
        outcsv.close()
        
##### Check if directories exist
if not os.path.exists(DATA_PATH):
    os.makedirs(DATA_PATH)
    os.makedirs(RESULTS_PATH)

headers = {
         #'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/98.0.4758.82 Safari/537.36',
        'user-agent' : 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/92.0.4515.107 Safari/537.36', 
        'Content-Type': 'application/json'
}

#CBET - BAFTA
#response = requests.get(url="https://nodejs08.tglab.io/cache/3/lt/lt/20228/prematch-by-tournaments.json?hidenseek=69815cb5ce8fb6f651be2e741a91a8c48695b945",
#                        headers=headers)
response = requests.get(url="https://nodejs08.tglab.io/cache/3/lt/lt/19817/prematch-by-tournaments.json?hidenseek=71d96d9ac3c4099896b35afa4070aa096847f0d4", headers=headers)

json_object = response.json()
print(response)
############ SAVE RAW FILE
# TODO:  Check if tournament is not null
raw_filename = 'cbet_' + strftime("%m_%d_%H_%M", gmtime()) + '.json'

print("Scraping "+sports+"...")

#with open("raw/"+sports+"/" + raw_filename, 'w') as outfile:
#    json.dump(json_object, outfile, indent=4)
   
for event in json_object['events'][0]['main_odds']['outright']['custom'].values():
    if not doesEventLogFileExist(sports):
        print("Log file for event",sports,"does not exist. Creating...")
        createNewEventLogFile(sports)

    csv_row = [strftime("%m_%d_%H_%M", gmtime())]
    csv_row.append(unidecode(event['name']))
    csv_row.append(unidecode(event['team_name']))
    csv_row.append(unidecode(event['odd_expr']))
    csv_row.append(event['odd_value'])

    with open(getEventFileName(sports), 'a', newline='') as outcsv:  # create this file
        writer = csv.writer(outcsv)
        writer.writerow(csv_row)





