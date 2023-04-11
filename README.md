# Gourmets.jp.rep

This a the repository of the python scripts created to help manage the orders, shipping etc.. in the eCommerce project Gourmets.jp.
The goal is just to show what I could code, find the easiest solutions to get the orders fulfilled quickly and at a minimum cost to start with. 
Obviously, the goal was to move to a professional service once the business was at full speed.

There is 3 main parts :
1. grab orders from Amazon using official APIs and store them in a file
  this was the easiest part since Amazon provide access to merchant store through a free set of APIs
 
2. grab orders from Rakuten using web scraping (with Selenium package) since APIs access was not free. 
Of course, this was the testing phase and I was planing to invest in a full stack later once the business in started at full speed.
But for the begining, this methode was easy enough to program and reliable to do the job for small quantities

3. Prepare shipment sticlers for Yamato
Same situation as Rakuten. To make it full automatic, it would require a contract with Yamato to access API and print directly. 
It was easier to start with Selenium to get everything working quickly and easily controllable by myself at no cost...

4. Some web scraping scripts to gather restaurant information when I approached them to sell Foie Gras in Kg.
