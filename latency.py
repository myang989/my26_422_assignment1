import subprocess
import csv
import re
import random
import matplotlib.pyplot as plt
import numpy as np

ip_addrs = []
with open('listed_iperf3_servers.csv', newline='') as f:
    reader = csv.DictReader(f)
    for row in reader:
        ip = row['IP/HOST']
        if not re.match(r'^(\d{1,3}\.){3}\d{1,3}$', ip):
            continue
        ip_addrs.append(ip)

random.shuffle(ip_addrs)  # shuffle once instead of random.choice each time
print(f"Read {len(ip_addrs)} IPs")

good = 0
results = {}

for test_ip in ip_addrs:
    if good >= 5:
        break
    try:
        print(f"traceroute {test_ip}")
        result = subprocess.run(
            ['traceroute', '-n', '-q', '1', '-w', '1', '-m', '20', test_ip],
            capture_output=True, text=True, timeout=30
        )
        output = result.stdout
    except subprocess.TimeoutExpired:
        print(f"SKIPPING {test_ip} — timed out")
        continue

    hops = []
    for line in output.splitlines()[1:]:
        parts = line.split()
        if not parts:
            continue
        if all(p == '*' for p in parts[1:]):
            continue
        hop = parts[0]
        rtts = [float(p) for p in parts[2:] if re.match(r'^\d+(\.\d+)?$', p)]
        if not rtts:
            continue
        avg_rtt = sum(rtts) / len(rtts)
        hops.append((hop, avg_rtt))

    if not hops:
        print(f"SKIPPING {test_ip} — no responsive hops")
        continue

    results[test_ip] = hops
    good += 1
    print(f"Got {good}/5 — {test_ip}")

print(f"Done. {good} responsive targets found.")


# build plots 
fig, ax = plt.subplots(figsize=(12, 8))
x = np.arange(len(results))  # one bar per destination ip
width = 0.5

# find max hops across all ips so we know how many layers to stack
max_hops = max(len(hops) for hops in results.values())

# build a 2d array: rows=hops, cols=ips
# each cell is the incremental rtt for that hop (diff from previous hop)
ips = list(results.keys())
hop_rtts = np.zeros((max_hops, len(ips)))

for col, ip in enumerate(ips):
    hops = results[ip]
    prev = 0
    for row, (hop, avg_rtt) in enumerate(hops):
        incremental = max(avg_rtt - prev, 0)  # diff from last hop
        hop_rtts[row][col] = incremental
        prev = avg_rtt

# stack the bars
bottoms = np.zeros(len(ips))
bars = []
for row in range(max_hops):
    b = ax.bar(x, hop_rtts[row], width, bottom=bottoms, label=f'Hop {row+1}')
    bars.append(b)
    bottoms += hop_rtts[row]

ax.set_xticks(x)
ax.set_xticklabels(ips, rotation=45, ha='right')
ax.set_ylabel('RTT (ms)')
ax.set_xlabel('Destination IP')
ax.set_title('Traceroute latency breakdown per hop')
ax.legend(loc='upper left', bbox_to_anchor=(1, 1))  # legend outside plot

plt.tight_layout()
plt.show()

#hop count vs rtt
fig, ax = plt.subplots(figsize=(10, 6))

for ip, hops in results.items():
    hop_count = len(hops)
    final_rtt = hops[-1][1]  # rtt of last hop = total rtt to destination
    ax.scatter(hop_count, final_rtt, s=100)
    ax.annotate(ip, (hop_count, final_rtt), textcoords="offset points", xytext=(8, 0))

ax.set_xlabel('Hop count')
ax.set_ylabel('Final RTT (ms)')
ax.set_title('Hop count vs RTT per destination IP')
plt.tight_layout()
plt.show()
    