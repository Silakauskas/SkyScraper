# Comment
# import libraries
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

DATA_PATH = "raw\\NBA\\"
RESULTS_PATH = "logs\\NBA\\"
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
        writer.writerow(["Date", event["teams"]["home"], "X", event["teams"]["away"], event['id']])
        outcsv.close()

headers = {
         'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:64.0) Gecko/20100101 Firefox/64.0',
         'Content-Type': 'application/json'
}

#ORAKULAS - NBA
response = requests.get(url="https://nodejs08.tglab.io/cache/3/lt/lt/394/prematch-by-championship.json",
                        headers=headers)

json_object = response.json()

############ SAVE RAW FILE
# TODO:  Check if tournament is not null
raw_filename = 'cbet_' + strftime("%m_%d_%H_%M", gmtime()) + '.json'

with open('raw/'+json_object['events'][0]['tournament_name']+'/' + raw_filename, 'w') as outfile:
    json.dump(json_object, outfile, indent=4)
   
for event in json_object['events']:
    if not doesEventLogFileExist(event['id']):
        print("Log file for event",event['id'],"does not exist. Creating...")
        createNewEventLogFile(event)
    
    csv_row = [raw_filename]
    
    for odd_id in event['main_odds']['main'].items():
        csv_row.append(odd_id[1]['odd_value'])
    
    csv_row.append(event['id'])
    
    with open(RESULTS_PATH + getEventFileName(event['id']), 'a') as outcsv:  # create this file
        writer = csv.writer(outcsv)
        writer.writerow(csv_row)





