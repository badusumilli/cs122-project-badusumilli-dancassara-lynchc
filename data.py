# CS122 Project: Dan Cassara, Connor Lynch, Bobby Adusumilli
# Functions to obtain historical investment data from Yahoo Finance
# and manipulate this data to get approprate portfolio data for 
# each allocation that we specify

import sqlite3
import pandas
from pandas.io.data import DataReader
import datetime
import time
import sys

# ticker_list = ['VTI', 'VBR', 'VEA', 'VTMGX', 'VWO', 'VSS', 'VNQ', 'VNQI', 'BND', 'VBMFX', 'BSV', 'VBISX', 'BNDX', 'VGTSX']

# VTI [('2001-06-15 00:00:00',)] Vanguard Total Stock Market ETF
# VBR [('2004-01-30 00:00:00',)] Vanguard Small-Cap Value ETF
# VEA [('2007-07-26 00:00:00',)] Vanguard FTSE Developed Markets ETF     	VTMGX
# VWO [('2005-03-10 00:00:00',)] Vanguard FTSE Emerging Markets ETF
# VSS [('2009-04-06 00:00:00',)] Vanguard FTSE All-World Ex-US Small Cap ETF 	
# VNQ [('2004-09-29 00:00:00',)] Vanguard REIT ETF
# VNQI [('2010-11-01 00:00:00',)] Vanguard Global Ex-US Real Estate ETF		
# BND [('2007-04-10 00:00:00',)] Vanguard Total Bond Market ETF				VBMFX
# BSV [('2007-04-10 00:00:00',)] Vanguard Short-Term Bond ETF				VBISX
# BNDX [('2013-06-04 00:00:00',)] Vanguard Total International Bond ETF		VGTSX



def retrieve_hist_prices(ticker):
	'''
	Function heavily obtained from http://stackoverflow.com/questions/12433076/
	download-history-stock-prices-automatically-from-yahoo-finance-in-python 

	This function allows to retrieve all historical pricing data, which 
	includes dividends and stock splits, for the Vanguard ETFs and mutual 
	funds from Yahoo Finance, and then create appropriate tables with the 
	data in sqlite3. 

	Input: 
		ticker_list: List of Vanguard ETFs and mutual funds to obtain 
			historical pricing data for

	Outputs: 
		sqlite3 tables with historical pricing data for each Vanguard 
			ETF / mutual fund
	'''
	connection = sqlite3.connect("roboadvisor.db")
	c = connection.cursor()

	# c.execute("DROP TABLE IF EXISTS " + ticker)
	# df = DataReader(ticker,  'yahoo', datetime.datetime(1980,1,1), datetime.datetime.now())

	# To get only most recent data
	last_date = c.execute("SELECT date FROM " + ticker + " ORDER BY date DESC LIMIT 1")
	last_date = last_date.fetchall()[0]
	last_date = datetime.datetime.strptime(last_date[0], '%Y-%m-%d %H:%M:%S')

	if last_date.date() < datetime.datetime.now().date() - datetime.timedelta(days=1):
		df = DataReader(ticker,  'yahoo', last_date + datetime.timedelta(days=1), datetime.datetime.now())
	
		dataframe = pandas.DataFrame(df)
		dataframe["Date"] = dataframe.index
		dataframe["Adj_Close"] = dataframe.pop("Adj Close")

	# http://pandas.pydata.org/pandas-docs/stable/generated/pandas.DataFrame.to_sql.html
		dataframe.to_sql(ticker, connection, if_exists='append', index=False)

	connection.commit()
	connection.close


# def drop_tables(ticker_list):
# 	connection = sqlite3.connect("roboadvisor.db")
# 	c = connection.cursor()
# 	for ticker in ticker_list:
# 		c.execute("DROP TABLE IF EXISTS " + ticker)
# 		c.execute("DROP TABLE IF EXISTS " + ticker + "_Distributions")

# 	# Get min dates
# 	for ticker in ticker_list:
# 		x = c.execute("SELECT MIN(DATE) FROM " + ticker +";")
# 		print(ticker, x.fetchall()) 

# 	connection.commit()
# 	connection.close


#######################################################################################333
if __name__=="__main__":
    num_args = len(sys.argv)

    # if num_args != 2:
    #     print("usage: python3 " + sys.argv[0] + " <file name for speaker A> " +
    #           "<file name for speaker B>\n  <file name of text to identify> " +
    #           "<order>")
    #     sys.exit(0)

    ticker = sys.argv[1]
    retrieve_hist_prices(ticker)
    
    # for index in range(1, num_args):

	   #  ticker = sys.argv[index]

	   #  # # print(ticker_list)
	   #  # print('arg 0: ', sys.argv[0])
	   #  # print('arg 1: ', sys.argv[1])
	   #  print(ticker)
	   #  retrieve_hist_prices(ticker)











