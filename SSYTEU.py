# -*- coding: utf-8 -*-

# API client library
import googleapiclient.discovery
import requests
import urllib3
import os
import os.path
from os import path
import json
import csv
from time import gmtime, strftime

sports = "EUROVISION_YT"
RESULTS_PATH = "logs"

if not os.path.exists(RESULTS_PATH):
    os.makedirs(RESULTS_PATH)

if (not path.exists("EUROVISION_YT.csv")):
    with open("EUROVISION_YT.csv", 'w') as outcsv: # create this file
        writer = csv.writer(outcsv)
        outcsv.close()

fileVidIds = open('/home/ubuntu/vidIds.txt', 'r')
lines = fileVidIds.read().splitlines()
#print(lines)

# API information
api_service_name = "youtube"
api_version = "v3"
# API key
DEVELOPER_KEY = "AIzaSyBlELBZq_ZCHo6-C1cCDklA1V5dal7qQPo"
# API client
youtube = googleapiclient.discovery.build(
        api_service_name, api_version, developerKey = DEVELOPER_KEY)

resp = requests.get(url="https://www.googleapis.com/youtube/v3/search?order=date&part=snippet&channelId=UCRpjHHu8ivVWs73uxHlWwFA&maxResults=50&key=AIzaSyBlELBZq_ZCHo6-C1cCDklA1V5dal7qQPo")

r = resp.text.encode('utf8').decode('ascii', 'ignore')
print(resp.status_code)
print(resp.url)
print(strftime("%m_%d_%H_%M", gmtime()))
print(" ")

#print(r)
json_object = json.loads(r)
for video in json_object["items"]:
    csv_row = [strftime("%m_%d_%H_%M", gmtime())]
    if "2022" in video["snippet"]["title"] and "videoId" in video["id"].keys():
        rv = youtube.videos().list(
            part="statistics,contentDetails",
            id=video["id"]["videoId"],
            fields="items(statistics,contentDetails(duration))"
        ).execute()
        
        #videoinfo = rv.text.encode('utf8').decode('ascii','ignore')
        #print(rv)
        
        csv_row.append(video["id"]["videoId"])
        csv_row.append(video["snippet"]["title"])
        csv_row.append(video["snippet"]["publishedAt"])
        csv_row.append(rv['items'][0]['statistics']['viewCount'])
        csv_row.append(rv['items'][0]['statistics']['likeCount'])
        csv_row.append(rv['items'][0]['statistics']['commentCount'])

        with open("EUROVISION_YT.csv", 'a', newline='') as outcsv: # create this file
            writer = csv.writer(outcsv)
            writer.writerow(csv_row)
            outcsv.close()
