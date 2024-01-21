# Personal-Python-Project
Summary: ticker_grabber.py scrapes the website Finviz.com to get stock ticker symbols & adds each ticker to my personal watchlists in my Webull.com trading account.

Entire code is separated into 3 functions:
loginWebull()
getDataFinviz(timeframe='wtd')
addToWebull(watchlist_type='wtd')

Problem: Finiviz.com is a free stock screener website that allows you to screen for stocks based on several technical & fundamental criteria. If you want to export the filtered data to excel, you need to pay a $24.96 monthly subscription. The site won't let you copy/paste information for free.

Solution: ticker_grabber uses Selenium Python Library to automatically:
1- login to my Webull account
2- Open new tab in Chrome & go to finviz.com
3- Get Top Gainer ticker symbols for different timeframes (Week-to-date, Month-to-date,Year-to-date) defined by the user as input parameter for "getDataFinviz(timeframe)" function. 
    Data Scraping is limited to either 3 pages or stock performance % (defined by the user), whichever comes first. 
4- Store each ticker symbol in Python List- named "finvizTickerList"
5- Go back to webull.com & search for the correct watchlist to add tickers to
6- Once correct watchlist is selected:
   Check if there are any tickers in the Webull Watchlist
     if there are tickers, check if those tickers are also in the finvizTickerList
       if tickers in Webull Watchlist are IN finvizTickerList then delete the ticker from finvizTickerList
       if tickers in Webull Watchlist are NOT IN finvizTickerList then delete the ticker from Webull Watchlist
     if there are no tickers in Webull Watchlist, then its empty and you dont have to delete anything

Personal Stock Screener Criteria I use to filter for top performing stocks:
1- Market Cap: 300M+
2- Average Daily Volume: >1M
3- Price > $5
4-Price above 200 DAY MOVING AVERAGE, 50 DAY MOVING AVERAGE, & 20 DAY MOVING AVERAGE

This screener is to find stocks that are:
1: Not penny stocks/pump n dump  (Price & Market Cap filter) 
2: Liquid/not thinly traded      (Volume filter)
3: In long term uptrend          (Moving Average filter) 



