# Part 1
## Answer to c:
From the scatter plot we can see a clear positive linear relationshipo betwween distance and rtt. As the distance increases from my location to the end destination ip, the round trip time increases. With the min rtt we can see the floor of the network speed which is limited by the physical distance. The max rtt can give an idea of the current network congestion. The range between min and max rtt was quite small. This indicated that the network state was quite stable.
## File of interest:
In the script ping_rtt.py, we loop though each valid ip address in the `listed_iperf3_servers.csv` and for each we:
1. Run ping 5 times and get max/min/avg rtt
2. Get the coord of the destination
3. Calculate the distance in km between our coord and the end destination coordinates.
Then we use create a plot using distance vs rtt.

# Part 2
## Answer to d:
We can see in the plots relating hop length and rtt, there is a dependent relationship between the two. This makes sense since the number of hops is independent from the physical distance between each intermidiate hop. For example we may have two destination ips: A and B. A might be physically located very far and B might be physcially very close (same city). We might have very few hops to A and many hops to B while the rtt of A is still greater. Higher hop count does not nessecarily mean higher rtt.  
## File of interest:
In the script latency.py, we again gather all of the valid ip addresses from the csv into a list. Randomize the list and loop though it until we have 5 valid trace routes collected. For each ip in the list, run a traceroute with a timeout=30sec and collect all valid (non "***") hop rtts. With all of this data for each of the 5 tracerouted destinations, we create a stacked bar graph showing its total ammount of rtts for all hopped locations. We also generate a scatter plot of the 5 destinations ips showing hop count vs rtt.