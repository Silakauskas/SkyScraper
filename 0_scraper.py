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

from bs4 import BeautifulSoup

headers = {
         'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:64.0) Gecko/20100101 Firefox/64.0',
         'Content-Type': 'application/json'
}

#ORAKULAS - NBA
response = requests.get(url="https://nodejs08.tglab.io/cache/3/lt/lt/394/prematch-by-championship.json",
                        headers=headers)
                        
print(response.headers, response.status_code)
json_object = response.json()
result = {}
print("  ",json_object['events'][0]['tournament_name'],"  ")

for event in json_object['events']:
        for odd_id in event['main_odds']['main'].items():
            if odd_id[1]['name'] == '1':
                print(event['teams']['home'], odd_id[1]['odd_value'])
            if odd_id[1]['name'] == 'X':
                print("X", odd_id[1]['odd_value'])
            if odd_id[1]['name'] == '2':
                print(event['teams']['away'], odd_id[1]['odd_value'])
        print(" ")


filename = 'data/'+json_object['events'][0]['tournament_name']+'/' + 'cbet_' + strftime("%m_%d_%H_%M", gmtime()) + '.json'


with open(filename, 'w') as outfile:
    json.dump(json_object, outfile, indent=4)
