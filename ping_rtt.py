import csv
import re
import requests
import time
from collections import defaultdict
import matplotlib.pyplot as plt
from geopy.distance import geodesic

# map for ip address to geo coord / times
# list index 0 stores the coord (lat,lon), index 1 has (min, rtt, max
ip_map = defaultdict(list)

with open('listed_iperf3_servers.csv', newline='') as f:
    reader = csv.DictReader(f)
    for row in reader:
        if not re.match(r'^(\d{1,3}\.){3}\d{1,3}$', row['IP/HOST']):
            # skip if not ip
            continue
        # if we have an ip, find its coords
        print(f"Mapping {row['IP/HOST']}")
        r = requests.get(f"http://ip-api.com/json/{row['IP/HOST']}", timeout=5)
        data = r.json()
        lat = data['lat']
        lon = data['lon']
        time.sleep(1.5)
        # add ip and coords to dict
        ip_map[row['IP/HOST']].append((lat, lon))

# read the bash script results in output.txt to add times to map
with open('output.txt') as f:
    for line in f:
        ip, min_val, avg_val, max_val = re.match(
            r'(\S+) min=([\d.]+)ms avg=([\d.]+)ms max=([\d.]+)ms', line
        ).groups()
        ip_map[ip].append((min_val, avg_val, max_val))
        
# now with the map we can construct the scatter plot
# my public IP is:
my_public_ip = requests.get('https://ifconfig.me').text.strip()
# lat lon is:
r = requests.get(f"http://ip-api.com/json/{my_public_ip}", timeout=5)
data = r.json()
lat_me = data['lat']
lon_me = data['lon']


for ip, val in ip_map.items():
    lat, lon = val[0]
    distance_km = geodesic((lat_me, lon_me), (lat, lon)).km
    val.append(distance_km)

# list index 0 stores the coord (lat,lon), index 1 has (min, rtt, max), index 2 has distance from me
distances = [val[2] for _, val in ip_map.items()]
rtt = [float(val[1][1]) for _, val in ip_map.items()]

plt.scatter(distances, rtt)
plt.xlabel('Distance (km) from my location')
plt.ylabel('rtt (avg of 5 pings)')
plt.title('Plot showing distance vs rtt for iperf3serverlist ip addresses')
plt.yticks(range(int(min(rtt)), int(max(rtt)) + 1, 50))  # tick every 50ms
plt.figure(figsize=(10, 8))
plt.show()