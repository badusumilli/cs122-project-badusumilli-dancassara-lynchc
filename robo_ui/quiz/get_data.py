# Robo-Advisor Project: Dan Cassara, Connor Lynch, Bobby Adusumilli

# This file contains functions to obtain historical investment data from 
# Yahoo Finance and store this data into the sqlite3 database roboadvisor.db

import sqlite3
import pandas
from pandas.io.data import DataReader

# We received a warning that pandas is creating a new datareader soon.
# If our code no longer works when graders are testing, the below package
# needs to be imported. Please let us know if this is a problem.
# from pandas_datareader import data, wb

import datetime
import sys


def retrieve_hist_prices(ticker):
	'''
	Modified from http://stackoverflow.com/questions/12433076/
	download-history-stock-prices-automatically-from-yahoo-finance-in-python 

	Allows to retrieve all historical pricing data, which includes dividends 
	and stock splits, for the Vanguard ETFs and mutual funds from Yahoo Finance, 
	and then creates appropriate tables with the data in roboadvisor.db. This 
	is updated daily through Cron

	Input: 
		ticker_list: List of Vanguard ETFs and mutual funds to obtain 
			historical pricing data for (ex: ['VTI', 'BND'])

	Outputs:
		sqlite3 roboadvisor.db tables with historical pricing data for each 
			Vanguard ETF / mutual fund (ex: 'BND')
	'''
	connection = sqlite3.connect("roboadvisor.db")
	c = connection.cursor()
	df = 'string'

	# Determine if table exists in sqlite3
	result = c.execute("select count(*) from sqlite_master where type='table' and name='" \
		+ ticker + "'")
	exists = result.fetchone()[0]

	if exists == 1:

		# To get only most recent data for table
		last_date = c.execute("SELECT Date FROM " + ticker + \
			" ORDER BY date DESC LIMIT 1")
		last_date = last_date.fetchone()[0]
		last_date = datetime.datetime.strptime(last_date, '%Y-%m-%d %H:%M:%S')

		# Determine most recent trading date of investment
		current = DataReader(ticker, 'yahoo', datetime.datetime.now() - \
			datetime.timedelta(days=5), datetime.datetime.now())
		current_df = pandas.DataFrame(current)
		current_df["Date"] = current_df.index
		current_date = datetime.datetime.strptime(str(current_df["Date"][-1]), \
			'%Y-%m-%d %H:%M:%S')

		if last_date.date() < current_date.date():
			df = DataReader(ticker,  'yahoo', last_date.date() + \
				datetime.timedelta(days=1), datetime.datetime.now())
	
	# Get all historical data for an investment if table not in roboadvisor.db
	else:
		df = DataReader(ticker,  'yahoo', datetime.datetime(1980, 1, 1), \
			datetime.datetime.now())
	
	# Only update roboadvisor.db table if necessary
	if type(df) != str:
		dataframe = pandas.DataFrame(df)
		dataframe["Date"] = dataframe.index
		dataframe["Adj_Close"] = dataframe.pop("Adj Close")

		# Code from: http://pandas.pydata.org/pandas-docs/stable/generated/
		# pandas.DataFrame.to_sql.html
		dataframe.to_sql(ticker, connection, if_exists = 'append', \
			index = False)

	connection.commit()
	connection.close


#######################################################################################
if __name__=="__main__":
    num_args = len(sys.argv)

    # if num_args != 2:
    #     print("error getting data")
    #     sys.exit(0)

    ticker = sys.argv[1]
    retrieve_hist_prices(ticker)
    
 