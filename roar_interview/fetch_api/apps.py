from django.apps import AppConfig
import requests
import threading
import time
import pymongo
from pymongo import MongoClient

class FetchApiConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'fetch_api'

    def ready(self):
        # Start timer in a backgroud thread avoid main thread sleeping.
        threading.Thread(target=self.setTimer, daemon=True, args=((self.fetchShowsApi, self.getDelaySecondsUntil11pm()))).start() 
        pass 

    def fetchShowsApi(self):
        # Fetch Shows API data
        response = requests.get('https://cloud.culture.tw/frontsite/trans/SearchShowAction.do?method=doFindTypeJ&category=1')
        # Process response to json
        showList = response.json()
        # Save the data into MongoDB
        cluster = MongoClient('mongodb://mongodb:27017') # mongodb://localhost:27017 for local machine, 'mongodb:27017' stands for service name + port
        db = cluster['roar_interview']
        collection = db['Shows']
        collection.insert_many(showList)

    def getDelaySecondsUntil11pm(self):
        # Get the current time
        currentTime = time.localtime() 
        # Calculate the delay until 11 p.m.
        delayHours = (23 - currentTime.tm_hour) % 24
        delayMinutes = (60 - currentTime.tm_min) % 60
        delaySeconds = (60 - currentTime.tm_sec) % 60

        delaySecondsUntil11pm = delayHours * 3600 + delayMinutes * 60 + delaySeconds
        return delaySecondsUntil11pm
    
    def setTimer(self, functionToCall, interval):
        # infinite loop for thread
        while True:
            print('Fetch Shows timer is set to 11pm.')
            # Thread sleep to avoid busy waiting
            time.sleep(interval)
            # Invoke input function to fetch Shows API
            functionToCall()