import requests
from google.transit import gtfs_realtime_pb2 as gtfsRTPB2
from dotenv import load_dotenv
import os


load_dotenv()

feed = gtfsRTPB2.FeedMessage()

def update():
    response = requests.get(
        url = "https://apis.metroinfo.co.nz/rti/gtfsrt/v1/vehicle-positions.pb",
        headers = {
            "Ocp-Apim-Subscription-Key": os.getenv("METRO_API_KEY")
        }
    )

    feed.ParseFromString(response.content)

class Pos:
    lat:int
    lon:int
    def __init__(self, x, y):
        self.lat=x
        self.lon=y

class Vehicle:
    pos:Pos
    route:str
    line_no:str
    updated:int

    def __init__(self, vehicleEntity):
        self.pos = Pos(vehicleEntity.position.latitude, vehicleEntity.position.longitude)
        self.route = vehicleEntity.trip.route_id
        self.line_no = self.route.split("_")[0]
        self.updated = vehicleEntity.timestamp


def retrieve_data():
    update()
    return [Vehicle(entity.vehicle) for entity in feed.entity]





update()
for entity in feed.entity:
    print(entity.vehicle.vehicle.id, end=',', )
    print(entity.vehicle.trip.trip_id, end=',', )
    print(entity.vehicle.trip.route_id, end=',', )
    # print(entity.vehicle.trip.direction_id, end=',')
    # print(entity.vehicle.trip.schedule_relationship, end=',', )
    print(entity.vehicle.position.latitude, entity.vehicle.position.longitude, end=',', )
    print(entity.vehicle.timestamp, end=',', )
    print()


"""
route ids:
1st no. is route number
2nd is...?
3rd is direction
    1,2 are north south
    3,4 are clockwise anticlockwise
    5,6 are east west
"""