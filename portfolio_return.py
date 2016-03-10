# CS122 Project: Dan Cassara, Connor Lynch, Bobby Adusumilli

# This file contains functions that create the historical performance graphs using
# the Python package Plotly

# http://stackoverflow.com/questions/19356920/embed-plotly-graph-into-a-webpage-with-bottle

import datetime
import sqlite3
# To install plotly for ipython3: 
# pip3 install --user plotly
import plotly.plotly as py
import plotly.tools as tls
import plotly.graph_objs as go
# Sign-In Info found in: https://plot.ly/settings/api
py.sign_in('badusumilli', 'lop4glzuu1')

TIME_DICT = {'1y': 'One', '5y': 'Five', '10y': 'Ten'}

ETF_NAMES = {
	'VTI': 'Vanguard Total Stock Market ETF', 
	'VBR': 'Vanguard Small-Cap Value ETF',
	'VEA': 'Vanguard FTSE Developed Markets ETF',   
	'VWO': 'Vanguard FTSE Emerging Markets ETF',
	'VSS': 'Vanguard FTSE All-World Ex-US Small Cap ETF', 
	'VNQ': 'Vanguard REIT ETF',
	'VNQI': 'Vanguard Global Ex-US Real Estate ETF',		
	'BND': 'Vanguard Total Bond Market ETF',			
	'BSV': 'Vanguard Short-Term Bond ETF',			
	'BNDX': 'Vanguard Total International Bond ETF'	
}

# Final potential recommended portfolios with Vanguard ETFs
ETF_ALLOCATION_DICT = { 
	'Very_Conservative': {'VTI': 0.10, 'VBR': 0.02,
	'VEA': 0.04, 'VWO': 0.01, 'VSS': 0.01, 'VNQ': 0.01, 'VNQI': 0.01,
	'BND': 0.48, 'BSV': 0.12, 'BNDX': 0.20},
	'Conservative': {'VTI': 0.20, 'VBR': 0.04,
	'VEA': 0.08, 'VWO': 0.02, 'VSS': 0.02, 'VNQ': 0.02, 'VNQI': 0.02,
	'BND': 0.36, 'BSV': 0.09, 'BNDX': 0.15},
	'Balanced': {'VTI': 0.30, 'VBR': 0.06,
	'VEA': 0.12, 'VWO': 0.03, 'VSS': 0.03, 'VNQ': 0.03, 'VNQI': 0.03,
	'BND': 0.24, 'BSV': 0.06, 'BNDX': 0.10},
	'Aggressive': {'VTI': 0.40, 'VBR': 0.08,
	'VEA': 0.16, 'VWO': 0.04, 'VSS': 0.04, 'VNQ': 0.04, 'VNQI': 0.04,
	'BND': 0.12, 'BSV': 0.03, 'BNDX': 0.05},
	'Very_Aggressive': {'VTI': 0.50, 'VBR': 0.10,
	'VEA': 0.20, 'VWO': 0.05, 'VSS': 0.05, 'VNQ': 0.05, 'VNQI': 0.05,
	'BND': 0.00, 'BSV': 0.00, 'BNDX': 0.00}
}


def create_graphs(allocation, wealth, worst_year_start_date, worst_year_end_date, best_year_start_date, best_year_end_date, hist_period = '10y'):
	'''
	Function to create necessary graphs for a user based on survey answers.

	Inputs: 
		allocation: our recommended allocation for a user (ex: 'Aggressive')
		hist_period: number of years for historical portfolio prices 
			(ex: '10y')
		wealth: starting money that person can invest (ex: 1000)

	Outputs:  
		annualized_return: annualized_return of user's recommended portfolio
			over hist_period
		list(ETF_NAMES.values()): Names of Vanguard ETFs
	'''
	connection = sqlite3.connect("roboadvisor.db")
	c = connection.cursor()

	# worst_year_change, worst_year_start_date, worst_year_end_date, best_year_change, best_year_start_date, best_year_end_date = find_worst_and_best_year(allocation, hist_period)

	allocation_bar_plotly(allocation)
	annualized_return = fund_performance_graph_plotly(allocation, wealth)
	graph_worst_year_plotly(allocation, wealth, worst_year_start_date, worst_year_end_date)
	graph_best_year_plotly(allocation, wealth, best_year_start_date, best_year_end_date)

	connection.commit()
	connection.close

	return annualized_return, list(ETF_NAMES.values())


def allocation_bar_plotly(allocation):
	'''
	Function to create interactive bar graph of our recommended portfolio
	allocation to a user using the Python package plotly. Code heavily
	borrowed from https://plot.ly/python/bar-charts/

	Input: 
		allocation: recommended allocation (ex: 'Aggressive')

	Output: 
		'User-Allocation': Interactive plotly bar graph of allocation
	'''
	funds = list(ETF_ALLOCATION_DICT[allocation].keys())
	percentages = [x * 100 for x in ETF_ALLOCATION_DICT[allocation].values()]

	data = [
	    go.Bar(
	        x = funds,
	        y = percentages,
	        marker = dict(
	            color = 'rgb(158,202,225)',
	            line = dict(
	                color = 'rgb(8,48,107)',
	                width = 1.5
	            ),
	        ),
	        opacity = 0.6
	    )
	]

	layout = go.Layout(
	    annotations = [
	        dict(
	            x = xi,
	            y = yi,
	            text = str(yi) + '%',
	            xanchor = 'center',
	            yanchor = 'bottom',
	            showarrow = False,
	        ) for xi, yi in zip(funds, percentages)], 
	     title = 'Your Portfolio Allocation: ' + allocation, 
	     yaxis = dict(
	     	title = 'Percentage of Portfolio (%)'),
	     xaxis = dict(
	     	title = 'Vanguard ETFs Ticker Symbols')
	)

	fig = go.Figure(data = data, layout = layout)
	plot_url = py.plot(fig, filename = 'User-Allocation')
	# tls.get_embed(py.plot_mpl(fig, filename='User-Allocation'))


def fund_performance_graph_plotly(allocation, wealth, hist_period = '10y'):
	'''
	Function to create interactive line graph of performance of user's 
	wealth invested in recommended allocation over past hist_period years
	using Python package plotly. Code heavily borrowed from 
	https://plot.ly/python/line-charts/

	Inputs: 
		allocation: recommended allocation (ex: 'Aggressive')
		wealth: starting money that person can invest (ex: 1000)
		hist_period: string of years for historical portfolio prices 
			(ex: '10y')

	Output: 
		'User-Portfolio-Performance': plotly interactive line graph of 
			person's growth in wealth of recommended allocation over 
			past hist_period years
	'''
	connection = sqlite3.connect("roboadvisor.db")
	c = connection.cursor()

	pf_prices = c.execute("SELECT * FROM " + allocation + "_" + TIME_DICT[hist_period] + "_Year_PF;")
	prices = pf_prices.fetchall()

	# Get dates in datetime format for label purposes
	date_list = [datetime.datetime.strptime(x[0], "%Y-%m-%d %H:%M:%S") for x in prices]
	price_list = [x[1] * wealth for x in prices]

	data = [
	    go.Scatter(
	        x = date_list,
	        y = price_list, 
	        line = dict(
	        	color = ('rgb(8,48,107)')
	        )
	    )
	]

	layout = go.Layout(
	     title = 'Your Estimated Growth in Wealth Over Past 10 Years: ' + allocation + ' Portfolio', 
	     yaxis = dict(
	     	title = 'Your Portfolio Value ($)'),
	     xaxis = dict(
	     	title = 'Year')
	)

	fig = go.Figure(data = data, layout = layout)
	plot_url = py.plot(fig, filename = 'User-Portfolio-Performance')
	# tls.get_embed(py.plot_mpl(fig, filename='User-Portfolio-Performance'))

	annualized_return = (((price_list[-1] / price_list[0]) ** (1 / int(hist_period[:-1]))) - 1) * 100
	return str("{0:.2f}".format(annualized_return)) + "%"


def graph_worst_year_plotly(allocation, wealth, worst_year_start_date, worst_year_end_date, hist_period = '10y'):
	'''
	Function to create interative line graph of person's decrease in wealth 
	over worst 12-month period over past hist_period years using Python 
	package plotly. Code heavily borrowed from 
	https://plot.ly/python/line-charts/

	Inputs: 
		allocation: recommended allocation (ex: 'Aggressive')
		wealth: starting money that person can invest (ex: 1000)
		worst_year_start_date: Start date of worst 12-month period
		worst_year_end_date: End date of worst 12-month period
		hist_period: string of years for historical portfolio prices 
			(ex: '10y')

	Output: 
		'User-Worst-Year': Interactive plotly line graph of worst 
			12-month performance of user's wealth with recommended 
			allocation
	'''
	connection = sqlite3.connect("roboadvisor.db")
	c = connection.cursor()

	# worst_year_change, worst_year_start_date, worst_year_end_date, best_year_change, best_year_start_date, best_year_end_date = find_worst_and_best_year(allocation, hist_period)
	pf_prices = c.execute("SELECT * FROM " + allocation + "_" + TIME_DICT[hist_period] + "_Year_PF WHERE Date >= '" + worst_year_start_date + "' AND Date <= '" + worst_year_end_date + "';")
	prices = pf_prices.fetchall()

	# Get dates in datetime format
	date_list = [datetime.datetime.strptime(x[0], "%Y-%m-%d %H:%M:%S") for x in prices]
	price_list = [(x[1] / prices[0][1]) * wealth for x in prices]

	data = [
	    go.Scatter(
	        x = date_list,
	        y = price_list,
	        line = dict(
	        	color = ('rgb(255, 69, 0)')
	        )
	    )
	]

	layout = go.Layout(
	     title = 'Worst 12-Month Performance Over Past 10 Years: ' + allocation + ' Portfolio', 
	     yaxis = dict(
	     	title = 'Your Portfolio Value ($)'),
	     xaxis = dict(
	     	title = 'Date')
	)

	fig = go.Figure(data = data, layout = layout)
	plot_url = py.plot(fig, filename = 'User-Worst-Year')
	# tls.get_embed(py.plot(fig, filename='User-Worst-Year'))

	# worst_return = ((price_list[-1] / price_list[0]) - 1) * 100
	# return str("{0:.2f}".format(worst_return)) + "%"


def graph_best_year_plotly(allocation, wealth, best_year_start_date, best_year_end_date, hist_period = '10y'):
	'''
	Function to create interative line graph of user's increase in wealth 
	over best 12-month period over past hist_period years using Python 
	package plotly. Code heavily borrowed from 
	https://plot.ly/python/line-charts/

	Inputs: 
		allocation: recommended allocation (ex: 'Aggressive')
		wealth: starting money that person can invest (ex: 1000)
		best_year_start_date: Start date of best 12-month period
		best_year_end_date: End date of best 12-month period
		hist_period: string of years for historical portfolio prices 
			(ex: '10y')

	Output: 
		'User-Best-Year': Interactive plotly line graph of best 
			12-month performance of user's wealth with recommended 
			allocation
	'''
	connection = sqlite3.connect("roboadvisor.db")
	c = connection.cursor()

	# worst_year_change, worst_year_start_date, worst_year_end_date, best_year_change, best_year_start_date, best_year_end_date = find_worst_and_best_year(allocation, hist_period)
	pf_prices = c.execute("SELECT * FROM " + allocation + "_" + TIME_DICT[hist_period] + "_Year_PF WHERE Date >= '" + best_year_start_date + "' AND Date <= '" + best_year_end_date + "';")
	prices = pf_prices.fetchall()

	# Get dates in datetime format
	date_list = [datetime.datetime.strptime(x[0], "%Y-%m-%d %H:%M:%S") for x in prices]
	price_list = [(x[1] / prices[0][1]) * wealth for x in prices]

	data = [
	    go.Scatter(
	        x = date_list,
	        y = price_list,
	        line = dict(
	        	color = ('rgb(8,48,107)')
	        )
	    )
	]

	layout = go.Layout(
	     title = 'Best 12-Month Performance Over Past 10 Years: ' + allocation + ' Portfolio', 
	     yaxis = dict(
	     	title = 'Your Portfolio Value ($)'),
	     xaxis = dict(
	     	title = 'Date')
	)

	fig = go.Figure(data = data, layout = layout)
	plot_url = py.plot(fig, filename = 'User-Best-Year')
	# tls.get_embed(py.plot(fig, filename='User-Best-Year'))

	# best_return = ((price_list[-1] / price_list[0]) - 1) * 100
	# return str("{0:.2f}".format(best_return)) + "%"
