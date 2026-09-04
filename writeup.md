# PLAN
-script to loop through the ip addresses and ping each and find the min max and avg (strip it)
-gather the geolocation coords of each location
-use numpy to make a scatter plot of distant vs rtt
-distance = from westlaf to point x
-pick 5 random ips, find the round trip time from my machine to each iternmediate hop along path with traceroute
-filter out non responsive hops.
-plot a stacked bar chart showing the breakdown of latencies to each hop.
-scatter plot hop count vs rtt. each data point is a destination ip.


# Part 1
## Answer to c:
From the scatter plot we can see a clear positive linear relationshipo betwween distance and rtt. As the distance increases from my location to the end destination ip, the round trip time increases. With the min rtt we can see the floor of the network speed which is limited by the physical distance. The max rtt can give an idea of the current network congestion. The range between min and max rtt was quite small. This indicated that the network state was quite stable.

# Part 2
## Answer to d:
We can see in the plots relating hop length and rtt, there is a dependent relationship between the two. This makes sense since the number of hops is independent from the physical distance between each intermidiate hop. For example we may have two destination ips: A and B. A might be physically located very far and B might be physcially very close (same city). We might have very few hops to A and many hops to B while the rtt of A is still greater. Higher hop count does not nessecarily mean higher rtt.  