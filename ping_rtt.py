import csv
import re
from geopy.geocoders import Nominatim


# initailize geolocator
geolocator = Nominatim(user_agent="ping_rtt_resolver")

# map for ip address to geo coord
ip_to_coord = {}

with open('listed_iperf3_servers.csv', newline='') as f:
    reader = csv.DictReader(f)
    for row in reader:
        if not re.match(r'^(\d{1,3}\.){3}\d{1,3}$', row['IP/HOST']):
            # skip if not ip
            continue
        # if we have an ip, find its coords
        location = geolocator.geocode(f"{row['COUNTRY']}, {row['SITE']}")
        # add ip and coords to dict
        ip_to_coord[row['IP/HOST']] = (location.latitude, location.longitude)

for i in ip_to_coord.items():
    print(i)