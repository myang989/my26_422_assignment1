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