# -*- coding: utf-8 -*-

# API client library
import googleapiclient.discovery
import requests
import urllib3
import json
# API information
api_service_name = "youtube"
api_version = "v3"
# API key
DEVELOPER_KEY = "AIzaSyBlELBZq_ZCHo6-C1cCDklA1V5dal7qQPo"
# API client
youtube = googleapiclient.discovery.build(
        api_service_name, api_version, developerKey = DEVELOPER_KEY)
# Request body
request = youtube.search().list(
        part="id,snippet",
        type='video',
        q="Spider-Man",
        videoDuration='short',
        videoDefinition='high',
        maxResults=1,
        fields="items(id(videoId),snippet(publishedAt,channelId,channelTitle,title,description))"
)

resp = requests.get(url="https://www.googleapis.com/youtube/v3/search?order=date&part=snippet&channelId=UCRpjHHu8ivVWs73uxHlWwFA&maxResults=20&key=AIzaSyBlELBZq_ZCHo6-C1cCDklA1V5dal7qQPo")

r = resp.text.encode('utf8').decode('ascii', 'ignore')
print(resp.status_code)
print(resp.url)
#print(r)
json_object = json.loads(r)
for video in json_object["items"]:
    rv = youtube.videos().list(
    part="statistics,contentDetails",
        id=video["id"]["videoId"],
        fields="items(statistics,contentDetails(duration))"
    ).execute()
    print(video["id"]["videoId"])
    print(video["snippet"]["title"])
    print(rv['items'][0]['statistics']['viewCount'])
    print(rv['items'][0]['statistics']['likeCount'])
    print(rv['items'][0]['statistics']['commentCount'])
    print(" ")
