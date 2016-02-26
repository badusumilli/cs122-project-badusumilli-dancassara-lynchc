# Obtain historical investment data from Yahoo Finance

import urllib.request
import sqlite3
import pandas
from pandas.io.data import DataReader
import datetime
import time

# ticker_list = ['VTI', 'VBR', 'VEA', 'VWO', 'VSS', 'VNQ', 'VNQI', 'BND', 'VTIP', 'BNDX']
# username = 'badusumilli'

# VTI [('2001-06-15 00:00:00',)] Vanguard Total Stock Market ETF
# VBR [('2004-01-30 00:00:00',)] Vanguard Small-Cap Value ETF
# VEA [('2007-07-26 00:00:00',)] Vanguard FTSE Developed Markets ETF
# VWO [('2005-03-10 00:00:00',)] Vanguard FTSE Emerging Markets ETF
# VSS [('2009-04-06 00:00:00',)] Vanguard FTSE All-World Ex-US Small Cap 	USE CRSP
# VNQ [('2004-09-29 00:00:00',)] Vanguard REIT ETF
# VNQI [('2010-11-01 00:00:00',)] Vanguard Global Ex-US Real Estate ETF
# BND [('2007-04-10 00:00:00',)] Vanguard Total Bond Market ETF
# VTIP [('2012-10-16 00:00:00',)] Vanguard Short-Term Inflation-Protected Securities ETF
# BNDX [('2013-06-04 00:00:00',)] Vanguard Total International Bond ETF


# Get dividend info: 
# http://stackoverflow.com/questions/28150076/python-pandas-recording-dividend-information-from-yahoo-finance
# https://ilmusaham.wordpress.com/tag/stock-yahoo-data/

# http://stackoverflow.com/questions/12433076/download-history-stock-prices-automatically-from-yahoo-finance-in-python
# http://stackoverflow.com/questions/2887878/importing-a-csv-file-into-a-sqlite3-database-table-using-python
# http://stackoverflow.com/questions/22991567/pandas-yahoo-finance-datareader


def pull_historical_data(ticker_list, username):

	connection = sqlite3.connect("roboadvisor.db")
	c = connection.cursor()

	for ticker in ticker_list:
		# base_url = "http://ichart.finance.yahoo.com/table.csv?s="
		output_path = "/home/" + username + "/Downloads"

		url = 'http://real-chart.finance.yahoo.com/table.csv?s=' + ticker + '&a=00&b=01&c=1980&d=01&e=7&f=2016&g=v&ignore=.csv'

		try:
			urllib.request.urlretrieve(url, output_path + "/" + ticker + "distributions.csv")

			# sql_query = 'create table ? (Date text, Open real, High real, Low real, Close real, Volume integer, Adjusted_Close real, constraint pk_? primary key (Date));'

			c.execute("DROP TABLE IF EXISTS " + ticker)
			c.execute("DROP TABLE IF EXISTS " + ticker + "_Distributions")
			# query = '.import ' + output_path + "/" + ticker + ".csv " + ticker

			# c.execute(query)

			dis = pandas.read_csv(output_path + "/" + ticker + "distributions.csv")

			pandas.DataFrame(dis).to_sql(ticker + '_Distributions', connection, schema='(Date TIMESTAMP, Dividends REAL)', if_exists='append', index=False)

			retrieve_hist_prices(ticker, connection)

		except urllib.request.ContentTooShortError as e:
			outfile = open(output_path + "/" + ticker + ".csv", "w")
			outfile.write(e.content)
			outfile.close()

	connection.commit()
	connection.close

	# return dis

def retrieve_hist_prices(ticker_list):
	connection = sqlite3.connect("roboadvisor.db")
	c = connection.cursor()

	for ticker in ticker_list:

		c.execute("DROP TABLE IF EXISTS " + ticker)
		c.execute("DROP TABLE IF EXISTS " + ticker + "_Distributions")
	# To manipulate start data:
	# df = DataReader(ticker,  'yahoo', datetime(1980,1,1), datetime(int(time.strftime('%Y')), \
	# 	int(time.strftime('%m')), int(time.strftime('%d'))))
		df = DataReader(ticker,  'yahoo', datetime.datetime(1980,1,1), datetime.datetime.now())

		# To get data only from past week
		# df = DataReader(ticker,  'yahoo', datetime.datetime.now() - datetime.timedelta(days = 7), datetime.now())
		# Timestamp('2016-01-04 00:00:00')
		dataframe = pandas.DataFrame(df)
		dataframe["Date"] = dataframe.index
		dataframe["Adj_Close"] = dataframe.pop("Adj Close")

	# http://pandas.pydata.org/pandas-docs/stable/generated/pandas.DataFrame.to_sql.html
		dataframe.to_sql(ticker, connection, if_exists='append', index=False)
	# return dataframe

def drop_tables(ticker_list):
	connection = sqlite3.connect("roboadvisor.db")
	c = connection.cursor()
	for ticker in ticker_list:
		c.execute("DROP TABLE IF EXISTS " + ticker)
		c.execute("DROP TABLE IF EXISTS " + ticker + "_Distributions")

def get_min_dates(ticker_list):
	connection = sqlite3.connect("roboadvisor.db")
	c = connection.cursor()

	for ticker in ticker_list:
		x = c.execute("SELECT MIN(DATE) FROM " + ticker +";")
		print(ticker, x.fetchall()) 




# dates = [datetime(y.year,y.month,y.day,y.hour,y.minute,y.second) for y in x.index]








