#!/bin/bash
{
    read -r _header
    while IFS=, read -r col1 _rest; do
        if ! [[ $col1 =~ ^([0-9]{1,3}\.){3}[0-9]{1,3}$ ]]; then
            continue
        fi
        echo "read $col1"
    done
} < listed_iperf3_servers.csv