#!/bin/bash
{
    read -r _header
    while IFS=, read -r col1 _rest; do
        if ! [[ $col1 =~ ^([0-9]{1,3}\.){3}[0-9]{1,3}$ ]]; then
            continue
        fi
        ping_output=$(ping -c 5 "$col1" 2>&1)  || { echo "$col1 unreachable"; continue; }
        stats=$(echo "$ping_output" | awk -F'[=/ ]+' '/round-trip/{print $6, $7, $8}')
        read -r min avg max <<< "$stats"
        echo "$col1 min=${min}ms avg=${avg}ms max=${max}ms"
    done
} < listed_iperf3_servers.csv | tee output.txt