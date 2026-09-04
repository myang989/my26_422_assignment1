#!/bin/bash
{
    read -r _header
    while IFS=, read -r col1 _rest; do
        echo "read $col1"
    done
} < listed_iperf3_servers.csv