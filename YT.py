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

sports = "EURO_YT"
RESULTS_PATH = "logs"

if not os.path.exists(RESULTS_PATH):
    os.makedirs(RESULTS_PATH)

if (not path.exists("EURO_YT.csv")):
    with open("EURO_YT.csv", 'w') as outcsv: # create this file
        writer = csv.writer(outcsv)
        outcsv.close()

print(" ")
fileVidIds = open('/home/ubuntu/vidIds.txt', 'r')
lines = fileVidIds.read().splitlines()
print("FIRST CHECK:",len(lines))
fileVidIds.close()

# API information
api_service_name = "youtube"
api_version = "v3"
# API key
DEVELOPER_KEY = "AIzaSyBlELBZq_ZCHo6-C1cCDklA1V5dal7qQPo"
# API client
youtube = googleapiclient.discovery.build(
        api_service_name, api_version, developerKey = DEVELOPER_KEY)

resp = requests.get(url="https://www.googleapis.com/youtube/v3/search?order=date&part=snippet&channelId=UCRpjHHu8ivVWs73uxHlWwFA&maxResults=60&key=AIzaSyBlELBZq_ZCHo6-C1cCDklA1V5dal7qQPo")

r = resp.text.encode('utf8').decode('ascii', 'ignore')
print(resp.status_code)
#print(resp.url)
print(strftime("%m_%d_%H_%M", gmtime()))
#print(r)
json_object = json.loads(r)
for video in json_object["items"]:
    csv_row = [strftime("%m_%d_%H_%M", gmtime())]
    if "2022" in video["snippet"]["title"] and "videoId" in video["id"].keys():
        if video["id"]["videoId"] not in lines:
            AppVidIds = open('/home/ubuntu/vidIds.txt', 'a', newline = '')
            AppVidIds.writelines(video["id"]["videoId"]+"\n")
            AppVidIds.close()

f = open('/home/ubuntu/vidIds.txt', 'r')
linesUpdated = f.read().splitlines()
print("SECOND CHECK", len(linesUpdated))
f.close()

for vidId in linesUpdated:
    csv_row = [strftime("%m_%d_%H_%M", gmtime())]
    rv = youtube.videos().list(
       part="snippet,statistics,contentDetails",
       id=vidId,
       fields="items(snippet(title,publishedAt),statistics,contentDetails(duration))"
    ).execute()
    #print(rv)
    csv_row.append(vidId)
    csv_row.append(rv['items'][0]["snippet"]["title"].encode('utf-8').decode('ascii','ignore'))
    csv_row.append(rv['items'][0]["snippet"]["publishedAt"])
    csv_row.append(rv['items'][0]['statistics']['viewCount'])
    csv_row.append(rv['items'][0]['statistics']['likeCount'])
    csv_row.append(rv['items'][0]['statistics']['commentCount'])

    with open("EURO_YT.csv", 'a', newline='') as outcsv: # create this file
        writer = csv.writer(outcsv)
        writer.writerow(csv_row)
        outcsv.close()
    
    csv_row = []
