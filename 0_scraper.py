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

sports = "ICE_HOCKEY"

DATA_PATH = "raw\\"+sports+"\\"
RESULTS_PATH = "logs\\"+sports+"\\"
TRACK_ENDED = True
odds = {}
finished = {}

def doesEventLogFileExist(event):
    return (getEventFileName(event) in os.listdir(RESULTS_PATH))

def getEventFileName(event):
    return str(event)+".csv"

def createNewEventLogFile(event):
    with open(RESULTS_PATH+getEventFileName(event['id']), 'w') as outcsv: # create this file
        writer = csv.writer(outcsv)
        writer.writerow(["Date", unidecode(event["teams"]["home"]), "X", unidecode(event["teams"]["away"]), event['date_start']])
        outcsv.close()

##### Check if directories exist
if not os.path.exists(DATA_PATH):
    print("Could not find directory.. Creating..")
    os.makedirs(DATA_PATH)
    os.makedirs(RESULTS_PATH)

headers = {
         'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/98.0.4758.81 Safari/537.36',
         'Content-Type': 'application/json'
}

#ORAKULAS - NBA
#response = requests.get(url="https://nodejs08.tglab.io/cache/3/lt/lt/394/prematch-by-championship.json",
#response = requests.get(url="https://nodejs08.tglab.io/cache/5/lt/lt/Europe-Vilnius/events-by-path.json?path=futbolas%7Cpasaulis%7Cpasaulio-cempionatas-2022-kvalifikacija-europa&hidenseek=9a78299aed2ce1444f657aab7fe9945bde4047b3",
response = requests.get(url="https://nodejs08.tglab.io/cache/3/lt/lt/14348/prematch-by-tournaments.json?hidenseek=82d1fedcdfd03ccf9504260c58e2e7b1830b029e",
                        headers=headers)

json_object = response.json()


############ SAVE RAW FILE
# TODO:  Check if tournament is not null
raw_filename = 'cbet_' + strftime("%m_%d_%H_%M", gmtime()) + '.json'

print("Scraping "+sports+"...")

#with open('raw/'+json_object['events'][0]['tournament_name']+'/' + raw_filename, 'w') as outfile:
with open("raw/"+sports+"/" + raw_filename, 'w') as outfile:
    json.dump(json_object, outfile, indent=4)
   
for event in json_object['events']:
    if not doesEventLogFileExist(event['id']):
        print("Log file for event",event['id'],"does not exist. Creating...")
        createNewEventLogFile(event)
    
    csv_row = [raw_filename]
    
    for odd_id in event['main_odds']['main'].items():
        csv_row.append(odd_id[1]['odd_value'])
    
    csv_row.append(event['id'])
    csv_row.append(event['date_start'])
    
    with open(RESULTS_PATH + getEventFileName(event['id']), 'a', newline='') as outcsv:  # create this file
        writer = csv.writer(outcsv)
        writer.writerow(csv_row)





