import csv
import re
import requests
import time
import subprocess
from collections import defaultdict
import matplotlib.pyplot as plt
from geopy.distance import geodesic

# map for ip address to geo coord / times
# list index 0 stores the coord (lat,lon), index 1 has (min, rtt, max
ip_map = defaultdict(list)

# my public IP is:
my_public_ip = requests.get('https://ifconfig.me').text.strip()
# lat lon is:
r = requests.get(f"http://ip-api.com/json/{my_public_ip}", timeout=5)
data_me = r.json()
lat_me = data_me['lat']
lon_me = data_me['lon']

with open('listed_iperf3_servers.csv', newline='') as f:
    reader = csv.DictReader(f)
    for row in reader:
        ip = row['IP/HOST']
        if not re.match(r'^(\d{1,3}\.){3}\d{1,3}$', ip):
            # skip if not ip
            continue

        # 1. run ping on ip
        result = subprocess.run(
            ['ping', '-c', '5', ip],
            capture_output=True, text=True
        )
        output = result.stdout + result.stderr
        m = re.search(r'round-trip|rtt[^=]*=\s*([\d.]+)/([\d.]+)/([\d.]+)', output)
        if not m:
            print(f"{ip} unreachable")
            continue
        
        min_rtt, avg_rtt, max_rtt = m.group(1), m.group(2), m.group(3)
        print(f"{ip} min={min_rtt}ms avg={avg_rtt}ms max={max_rtt}ms")

        ip_map[ip].append({
            'min': float(min_rtt),
            'avg': float(avg_rtt),
            'max': float(max_rtt)
        })

        # 2. get coord for ip
        print(f"Mapping {ip}")
        r = requests.get(f"http://ip-api.com/json/{ip}", timeout=5)
        data = r.json()
        lat = data['lat']
        lon = data['lon']
        time.sleep(1)

        # 3. calc distance
        distance_km = geodesic((lat_me, lon_me), (lat, lon)).km
        ip_map[ip].append(distance_km)


# list index 0 stores (min, rtt, max), index 1 has distance from me
distances = [val[1] for _, val in ip_map.items()]
rtt = [val[0]['avg'] for _, val in ip_map.items()]

plt.scatter(distances, rtt)
plt.xlabel('Distance (km) from my location')
plt.ylabel('rtt (avg of 5 pings)')
plt.title('Plot showing distance vs rtt for iperf3serverlist ip addresses')
plt.yticks(range(int(min(rtt)), int(max(rtt)) + 1, 25))
plt.show()