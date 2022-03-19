import csv
import pandas as pd

# openstreet map api
from geopy.geocoders import Nominatim
geolocator = Nominatim(user_agent="user_agent_1")


#load csv names into lists
airports = []
airfields = []

with open('./airport_name.csv', newline='') as csvfile:
    aiport_csv = csv.reader(csvfile, delimiter=',', quotechar="'")
    next(aiport_csv)
    for row in aiport_csv:
        if len(row) > 0:
            airports.append(row[0])

with open('./airfield_name.csv', newline='') as csvfile:
    aifield_csv = csv.reader(csvfile, delimiter=',', quotechar="'")
    next(aifield_csv)
    for row in aifield_csv:
        if row[1] != "":
            airfields.append(row[1])
        else:
            airfields.append(row[0])

#1442 international public airports vs. 661 military-built airfields
#chinese airports are not distinct names of airports so coordinates are used
print(len(airports))
print(len(airfields))

airports_wkt = []
airfields_wkt = []


#change names to WKT coordinates
for i in airports:
    try:
        location = geolocator.geocode(i)
    except Exception as e:
        print(e)
        pass
    if hasattr(location, "latitude"):
        airports_wkt.append(f"POINT ( {location.latitude} {location.longitude} )")
        print(f"POINT ( {location.latitude} {location.longitude} )")

for i in airfields:
    try:
        location = geolocator.geocode(i)
    except Exception as e:
        print(e)
        pass
    if hasattr(location, "latitude"):
        airfields_wkt.append(f"POINT ( {location.latitude} {location.longitude} )")
        print(f"POINT ( {location.latitude} {location.longitude} )")

print(airfields_wkt)

pd.DataFrame(airports_wkt).to_csv('./airport_WKT.csv')
pd.DataFrame(airfields_wkt).to_csv('./airfield_WKT.csv')