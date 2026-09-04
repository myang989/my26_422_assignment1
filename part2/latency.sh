#!/bin/bash

output_file="traceroute_results.txt"
> "$output_file"

# randomized set of ips
ips=(
     "105.235.237.2"
    "197.227.12.18"
    "41.210.185.162"
    "185.93.1.65"
    "160.242.19.254"
    "23.249.58.14"
    "169.150.202.193"
    "69.48.239.124"
    "23.249.55.42"
    "69.48.238.200"
    "148.230.60.200"
    "189.25.101.151"
    "41.110.39.130"
    "213.158.175.240"
    "102.214.66.39"
    "102.214.66.19"
    "212.60.92.134"
    "84.17.57.129"
    "189.25.97.217"
    "185.102.219.93"
    "185.59.221.51"
    "109.61.94.65"
    "49.205.75.2"
)
good=0

for ip in "${ips[@]}"; do
    [[ $good -ge 5 ]] && break

    echo "Testing $ip..."
    result=$(traceroute -n -q 3 -w 2 "$ip" 2>/dev/null)

    # check if final destination responded — last hop should contain the target ip
    if ! echo "$result" | tail -5 | grep -q "$ip"; then
        echo "SKIPPING $ip — did not reach destination"
        continue
    fi

    echo "TARGET:$ip" >> "$output_file"
    echo "$result" | tail -n +2 | while IFS= read -r line; do
        [[ "$line" =~ ^\s*[0-9]+\s+\*" "\*" "\* ]] && continue
        hop=$(echo "$line" | awk '{print $1}')
        hop_ip=$(echo "$line" | awk '{print $2}')
        avg_rtt=$(echo "$line" | awk '{
            sum=0; count=0
            for(i=3; i<=NF; i++) {
                if ($i ~ /^[0-9]+(\.[0-9]+)?$/) { sum+=$i; count++ }
            }
            if (count > 0) printf "%.3f", sum/count
        }')
        [[ -z "$avg_rtt" ]] && continue
        echo "HOP:$hop IP:$hop_ip RTT:${avg_rtt}ms" >> "$output_file"
    done
    echo "---" >> "$output_file"

    ((good++))
    echo "Got $good/5 good targets"
done

echo "Done. $good responsive targets recorded."