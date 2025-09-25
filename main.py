import requests
from google.transit import gtfs_realtime_pb2 as gtfsRTPB2
from dotenv import load_dotenv
import os

load_dotenv()

feed = gtfsRTPB2.FeedMessage()
response = requests.get(
    url = "https://apis.metroinfo.co.nz/rti/gtfsrt/v1/vehicle-positions.pb",
    headers = {
        "Ocp-Apim-Subscription-Key": os.getenv("METRO_API_KEY")
    }
)

print(response.content)

feed.ParseFromString(response.content)
for entity in feed.entity:
    if entity.HasField('trip_update'):
        print(entity.trip_update)
    print(entity.vehicle.position.latitude, entity.vehicle.position.longitude)