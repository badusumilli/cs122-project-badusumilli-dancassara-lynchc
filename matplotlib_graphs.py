import urllib.request
import sqlite3
import pandas
from pandas.io.data import DataReader
import datetime
import time

import numpy as np
import matplotlib.pyplot as plt

# To install plotly for ipython3: 
# pip3 install --user plotly
import plotly.plotly as py
import plotly.tools as tls
import plotly.graph_objs as go

# ticker_list = ['VTI', 'VBR', 'VEA', 'VTMGX', 'VWO', 'VSS', 'VNQ', 'VNQI', 'BND', 'VBMFX', 'BSV', 'VBISX', 'BNDX', 'VGTSX']

# VTI [('2001-06-15 00:00:00',)] Vanguard Total Stock Market ETF
# VBR [('2004-01-30 00:00:00',)] Vanguard Small-Cap Value ETF
# VEA [('2007-07-26 00:00:00',)] Vanguard FTSE Developed Markets ETF     	VTMGX
# VWO [('2005-03-10 00:00:00',)] Vanguard FTSE Emerging Markets ETF
# VSS [('2009-04-06 00:00:00',)] Vanguard FTSE All-World Ex-US Small Cap 	USE CRSP
# VNQ [('2004-09-29 00:00:00',)] Vanguard REIT ETF
# VNQI [('2010-11-01 00:00:00',)] Vanguard Global Ex-US Real Estate ETF		SPBMGUU S&P Global Ex-US Property
# BND [('2007-04-10 00:00:00',)] Vanguard Total Bond Market ETF				VBMFX
# BSV [('2007-04-10 00:00:00',)] Vanguard Short-Term Bond ETF				VBISX
# BNDX [('2013-06-04 00:00:00',)] Vanguard Total International Bond ETF		VGTSX


# Get dividend info: 
# http://stackoverflow.com/questions/28150076/python-pandas-recording-dividend-information-from-yahoo-finance
# https://ilmusaham.wordpress.com/tag/stock-yahoo-data/

# http://stackoverflow.com/questions/12433076/download-history-stock-prices-automatically-from-yahoo-finance-in-python
# http://stackoverflow.com/questions/2887878/importing-a-csv-file-into-a-sqlite3-database-table-using-python
# http://stackoverflow.com/questions/22991567/pandas-yahoo-finance-datareader

# dates = [datetime(y.year,y.month,y.day,y.hour,y.minute,y.second) for y in x.index]


def allocation_bar(allocation, save_to = None):
	# http://matplotlib.org/examples/api/barchart_demo.html
	# http://matplotlib.org/examples/pylab_examples/barchart_demo.html
	funds = list(ETF_ALLOCATION_DICT[allocation].keys())
	percentages = [x * 100 for x in ETF_ALLOCATION_DICT[allocation].values()]

	width = 0.35
	y_pos = np.arange(len(funds))

	# fig = plt.figure(figsize = (8,8)) 
	fig, ax = plt.subplots()
	# ax = fig.add_axes([0.1, 0.2, 0.7, 0.7])
	# colors: http://matplotlib.org/examples/color/named_colors.html
	ax.set_xlabel('Portfolio Percentage (%)')
	ax.set_ylabel('Vanguard ETF Ticker')
	ax.set_yticks(y_pos)
	ax.set_yticklabels(funds)
	ax.set_title('Your Portfolio Allocation: ' + allocation)
	ax.set_xlim(0, 1.1 * max(percentages))
	ax.set_ylim(-1, len(funds))

	rects = ax.barh(y_pos, percentages, 0.65, align='center', color = 'thistle')

	for rect in rects: 
		ax.text(rect.get_width() + 0.40, rect.get_y() + rect.get_height()/4., rect.get_width())

	if save_to is None: 
		plt.show()
	else: 
		fig.savefig(save_to)

	# plot_url = py.plot_mpl(fig, filename='User-Allocation')
	# tls.get_embed(py.plot_mpl(fig, filename='User-Allocation'))


def fund_performance_graph(allocation, hist_period, wealth, save_to = None):
	connection = sqlite3.connect("roboadvisor.db")
	c = connection.cursor()

	pf_prices = c.execute("SELECT * FROM " + allocation + "_" + TIME_DICT[hist_period] + "_Year_PF;")
	prices = pf_prices.fetchall()
	date_list = [datetime.datetime.strptime(x[0], "%Y-%m-%d %H:%M:%S") for x in prices]
	price_list = [x[1] * wealth for x in prices]
	x_pos = np.arange(len(date_list))

	# fig = plt.figure(figsize = (8,8))
	# ax = fig.add_axes([0.1, 0.2, 0.85, 0.75])

	fig, ax = plt.subplots()

	ax.plot(date_list, price_list, color = 'skyblue')
	ax.fill_between(date_list, price_list, facecolor='skyblue', alpha = 0.5, lw=0.5)

	ax.set_ylim(min(price_list) - (wealth // 10), max(price_list) + (wealth // 10))
	ax.set_xlabel('Year')
	ax.set_ylabel('Portfolio Value ($)')
	ax.set_title(allocation + " Past " + hist_period[:-1] + "-Year Portfolio Performance")

	# ax.text(1000, 2500, 'Value After 10 Years: ' + str(price_list[-1]), fontsize=10)

	# if save_to is None: 
	# 	plt.show()
	# else: 
	# 	fig.savefig(save_to)

	plot_url = py.plot_mpl(fig, filename='User-Portfolio-Performance')
	# tls.get_embed(py.plot_mpl(fig, filename='User-Portfolio-Performance'))


def graph_worst_year(allocation, hist_period, wealth, save_to = None):
	connection = sqlite3.connect("roboadvisor.db")
	c = connection.cursor()

	worst_year_change, worst_year_start_date, worst_year_end_date, best_year_start_date, best_year_end_date, best_year_change = find_worst_and_best_year(allocation, hist_period)
	pf_prices = c.execute("SELECT * FROM " + allocation + "_" + TIME_DICT[hist_period] + "_Year_PF WHERE Date >= '" + worst_year_start_date + "' AND Date <= '" + worst_year_end_date + "';")
	prices = pf_prices.fetchall()
	date_list = [datetime.datetime.strptime(x[0], "%Y-%m-%d %H:%M:%S") for x in prices]
	price_list = [(x[1] / prices[0][1]) * wealth for x in prices]
	x_pos = np.arange(len(date_list))

	# fig = plt.figure(figsize = (8,8))
	# ax = fig.add_axes([0.1, 0.2, 0.85, 0.75])

	fig, ax = plt.subplots()

	ax.plot(date_list, price_list, color = 'red')
	ax.fill_between(date_list, price_list, facecolor='red', alpha = 0.5, lw=0.5)


	ax.set_ylim(min(price_list) - (wealth // 10), max(price_list) + (wealth // 10))
	ax.set_xlabel('Year')
	ax.set_ylabel('Portfolio Value ($)')
	ax.set_title(allocation + " Worst 12 Month Performance Over Past 10 Years")

	# http://stackoverflow.com/questions/10998621/rotate-axis-text-in-python-matplotlib
	for tick in ax.get_xticklabels():
		tick.set_rotation(90)

	# if save_to is None: 
	# 	plt.show()
	# else: 
	# 	fig.savefig(save_to)

	plot_url = py.plot_mpl(fig, filename='User-Worst-Year')
	# tls.get_embed(py.plot_mpl(fig, filename='User-Worst-Year'))



def pull_historical_data(ticker_list, username):

	connection = sqlite3.connect("roboadvisor.db")
	c = connection.cursor()

	for ticker in ticker_list:
		# base_url = "http://ichart.finance.yahoo.com/table.csv?s="
		output_path = "/home/" + username + "/Downloads"

		url = 'http://real-chart.finance.yahoo.com/table.csv?s=' + ticker + '&a=00&b=01&c=1980&d=01&e=7&f=2016&g=v&ignore=.csv'
		# url = 'http://real-chart.finance.yahoo.com/table.csv?s=VBR&a=00&b=01&c=1980&d=01&e=7&f=2016&g=v&ignore=.csv'

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


def pull_hist_data(username):
	url = 'http://us.spindices.com/idsexport/file.xls?hostIdentifier=48190c8c-42c4-46af-8d1a-0cd5db894797&selectedModule=PerformanceGraphView&selectedSubModule=Graph&yearFlag=tenYearFlag&indexId=5532268'
	output_path = "/home/" + username + "/Downloads"
	urllib.request.urlretrieve(url, output_path + "/RE_ex_US.csv")