# col-n
Mostly python data and crypto stuff.

So far I have four projects. More on the way.

1. An analysis of LendingClub portfolios (ipython notebook).  Here, I examine in detail some of the factors that Lending Club could be using to identify risky borrowers (with only data provided by Lending Club, not external data).  This analysis may also help identify potentially mis-priced loans; that is, loans of a given yield that are not necessarily the same risk.

2. A geospacial analysis of zip code and price data (ipython notebook).  This notebook takes zipcodes and translates them to Latitude-Longitude using Google's API.  Then, a simple cluster analysis is performed on the lat-long data using scipy's kmeans2. Finally, this notebook creates a KML file that can be viewed in Google Earth, with some custom features to aid analysis based on the price. 

3. An RSA implementation in python (python file).  Creates public and private keys from pseudo-random numbers of 5-32 bits using systemrandom, the crytpographically acceptable method. Tests for primality using the Miller-Rabin algo.  Includes a (very) simple function to decompose the resulting semi-prime 'n' back into the prime factors to demonstrate the increasing returns to bit-length of 'n' (hint: its much harder the longer they are).  

4. The Matasano Crypto Challenges (series of ipython notebooks and python files).  I'm working on the challenges and posting them here when I am satisfied with them.
