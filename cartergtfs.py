from datetime import datetime
from bs4 import BeautifulSoup
import requests
import time


from google.transit import gtfs_realtime_pb2
import urllib


class Trains:
  def __init__(self, label, stop_id, route_id):
    self.label = label
    self.stop_id = stop_id
    self.route_id = route_id
    self.arrival_times = []


trains = [Trains("Uptown 2", "232N","2"),
Trains("Uptown 3", "232N","3"),
Trains("Uptown 4", "423N","4"),
Trains("Uptown 5", "423N","5"),
Trains("Downtown 2", "232S","2"),
Trains("Downtown 3", "232S","3"),
Trains("Downtown 4", "423S","4"),
Trains("Downtown 5", "423S","5")]

def GetTimes():
    for tr in trains:
        tr.arrival_times = []
    feed = gtfs_realtime_pb2.FeedMessage()
    response = urllib.request.urlopen('http://datamine.mta.info/mta_esi.php?key=581ad7b399d1eddcccec3a31d0e6e00d&feed_id=1')
    feed.ParseFromString(response.read())
    now = datetime.now()
    for entity in feed.entity:
        if entity.HasField('trip_update'):
            for stu in entity.trip_update.stop_time_update:
                for tr in trains:
                    if stu.stop_id == tr.stop_id and entity.trip_update.trip.route_id[0] == tr.route_id[0]:
                        mintoarrive = (datetime.fromtimestamp(stu.arrival.time)-now).total_seconds()/60
                        if mintoarrive >= 0:
                            tr.arrival_times.append(round(mintoarrive,0))
                        break
    for tr in trains:
        tr.arrival_times.sort()

def DisplayTimes():
    for i in range(100):
        print()
    print("Uptown")
    # for tr in trains:
    #     print(tr.route_id, tr.arrival_times[0])
    i = 0
    j = 4
    while i < 4:
        if len(trains[i].arrival_times) != 0:
            print(trains[i].route_id, int(trains[i].arrival_times[0]), "min")
        i += 1
    print("Downtown")
    while j < 8:
        if len(trains[j].arrival_times) != 0:
            print(trains[j].route_id, int(trains[j].arrival_times[0]), "min")
        j += 1

def Main():
    for i in range(1,10):
        GetTimes()
        DisplayTimes()
        time.sleep(15)
Main()
