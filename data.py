# Obtain historical investment data from Yahoo Finance

import urllib
import sqlite3

# ETFS = ['VTI', 'VBR', 'VEA', 'VWO', 'VSS', 'VNQ', 'VNQI', 'BND', 'VTIP', 'BNDX']


def pull_historical_data(ticker_list, username, directory="S&P"):

	# from http://stackoverflow.com/questions/12433076/download-history-stock-prices-automatically-from-yahoo-finance-in-python
	
	for ticker in ticker_list:
		base_url = "http://ichart.finance.yahoo.com/table.csv?s="
		output_path = "/home/" + username + "/Downloads"

		try:
			urllib.request.urlretrieve(base_url + ticker, output_path + "/" + ticker + ".csv")
			connection = sqlite3.connect("roboadvisor.db")
			c = connection.cursor()
			sql_query = 'create table ? (Date text, Open real, High real, Low real, Close real, ' + /
				'Volume integer, Adjusted_Close real, constraint pk_? primary key (Date));'
			c.execute(sql_query, [ticker, ticker])
			query = '.import ? ?'
			c.execute(query, [output_path + "/" + ticker + ".csv", ticker])
			# header = get_header(c)
			# results = output.fetchall()
			connection.close

		except urllib.request.ContentTooShortError as e:
			outfile = open(make_filename(ticker, directory), "w")
			outfile.write(e.content)
			outfile.close()