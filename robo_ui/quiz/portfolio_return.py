# Roboadvisor Project: Dan Cassara, Connor Lynch, Bobby Adusumilli

# This file contains functions to create the interactive historical performance 
# graphs using the Python package Plotly

import datetime
import sqlite3
import json
# To install plotly for ipython3: 
# pip3 install --user plotly
import plotly.plotly as py
import plotly.tools as tls
import plotly.graph_objs as go
# To sign into Plotly: https://plot.ly/settings/api
py.sign_in('badusumilli', 'lop4glzuu1')

TIME_DICT = {'1y': 'One', '5y': 'Five', '10y': 'Ten'}

# All of the ETFs that we recommend
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


def create_graphs_and_text(allocation, wealth, hist_period ='10y'):
	'''
	Original function

	Function to create necessary graphs for a user based on survey answers.
	Also creates the necessary text that will display on results webpage. 

	Inputs: 
		allocation: our recommended allocation for a user (ex: 'Aggressive')
		wealth: starting money that person can invest (ex: 1000)
		hist_period: number of years for historical portfolio prices 
			(ex: '10y')

	Outputs:  
		plotly graphs specific to the user
		json files with the text necessary for the results webpage
	'''
	connection = sqlite3.connect("roboadvisor.db")
	c = connection.cursor()

	best_worst = c.execute("SELECT * FROM Best_Worst_Year WHERE Allocation = '" \
		+ allocation + "'")
	bw = best_worst.fetchall()[0]
	worst_change = bw[1]
	worst_year_start_date = bw[2]
	worst_year_end_date = bw[3]
	best_change = bw[4]
	best_year_start_date = bw[5]
	best_year_end_date = bw[6]

	# Create the 4 graphs for the website for the user's specific info
	allocation_bar_plotly(allocation)
	annualized_return = fund_performance_graph_plotly(allocation, wealth)
	graph_worst_year_plotly(allocation, wealth, worst_year_start_date, \
		worst_year_end_date)
	graph_best_year_plotly(allocation, wealth, best_year_start_date, \
		best_year_end_date)

	connection.commit()
	connection.close

	# Create descriptions to be displayed on the website
	allocation_text, etfs_text, performance_text, worst_text, best_text = \
		create_descriptions(allocation, annualized_return, worst_change, \
		best_change)

	# Create json file with all of the text for results webpage
	with open('quiz/temp_json_files/allocation_text.txt', 'w') as outfile: 
		json.dump(allocation_text, outfile)

	with open('quiz/temp_json_files/etfs_text.txt', 'w') as outfile: 
		json.dump(etfs_text, outfile)

	with open('quiz/temp_json_files/performance_text.txt', 'w') as outfile: 
		json.dump(performance_text, outfile)

	with open('quiz/temp_json_files/worst_text.txt', 'w') as outfile: 
		json.dump(worst_text, outfile)

	with open('quiz/temp_json_files/best_text.txt', 'w') as outfile: 
		json.dump(best_text, outfile)	

	with open('quiz/temp_json_files/profile.txt', 'w') as outfile:
		json.dump(allocation, outfile)


def create_descriptions(allocation, annualized_return, worst_change, best_change):
	'''
	Original function

	Create necessary description for results webpage for user

	Inputs: 
		allocation: specific allocation (ex: 'Aggressive')
		annualized_return: string of annual return over past 10 years for 
			the allocation (ex: '5.0%')
		worst_change: string of worst 12-month return over the past 10 
			years for the allocation (ex: '-50.0%')
		best_change: string of worst 12-month return over the past 10 
			years for the allocation (ex: '60.0%')

	Outputs: 
		allocation_text: Text for top of webpage explaining allocation
		etfs_text: Names of each of the recommended ETFs
		performance_text: Text of annualized performance of allocation 
			over past ten years
		worst_text: Text explaining worst 12-month period of allocation 
			over past 10 years
		best_text: Text explaining best 12-month period of allocation 
			over past 10 years
	'''
	allocation_text = "This portfolio consists of Vanguard ETFs, chosen because " \
	+ "Vanguard offers some of the best-performing ETFs at the lowest costs¹. " \
	+ "This allocation was chosen for you based on your assessed risk " \
	+ "tolerance. In order to expect a higher return over " \
	+ "the next 10 years, you would need to take on more risk by increasing " \
	+ "the portion of your invested wealth allocated in equities. Below " \
	+ "are graphs illustrating how the portfolio performed over the previous " \
	+ "10 years. While there are never any guarantees in investing, an investor " \
	+ "can expect to have a similar experience over the next 10 years."

	etfs = []
	for etf in ETF_NAMES.items():
		etfs.append(etf[0] + ": " + etf[1])
	etfs_text = ', '.join(etfs)

	performance_text = "Over the past 10 years, this portfolio grew " \
	+ annualized_return + " annually." 

	worst_text = "The worst 12-month return of the " + allocation + " Portfolio " \
	+ "over the past 10 years was " + worst_change + ". With this allocation, " \
	+ "it is possible that a similar 12-month period may occur within the next " \
	+ "10+ years. In order to be a successful investor, it is important " \
	+ "to stay invested, even during down markets, because it is impossible to " \
	+ "predict how or when the market will move in the future. If you would be " \
	+ "overly uncomfortable seeing this drop in your wealth, you may want to " \
	+ "select a portfolio that takes on less risk. To do so, click on the Less " \
	+ "Aggressive link below."

	best_text = "The best 12-month return of the " + allocation + " Portfolio " \
	+ "over the past 10 years was " + best_change + ". If you would like to " \
	+ "increase the expected return of your portfolio, it is necessary to " \
	+ "take on additional risk in your portfolio. If you think that you can " \
	+ "tolerate a higher level of risk in your portfolio, click on the More " \
	+ "Aggressive link below."

	return allocation_text, etfs_text, performance_text, worst_text, best_text


def allocation_bar_plotly(allocation):
	'''
	Modified from https://plot.ly/python/bar-charts/

	Function to create interactive bar graph of our recommended portfolio
	allocation to a user using the Python package plotly. 

	Input: 
		allocation: recommended allocation (ex: 'Aggressive')

	Output: 
		'User-Allocation': Interactive plotly bar graph of allocation.
			First graph on results webpage
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
	plot_url = py.plot(fig, filename = 'User-Allocation', auto_open = False)


def fund_performance_graph_plotly(allocation, wealth, hist_period = '10y'):
	'''
	Modified from https://plot.ly/python/line-charts/

	Create interactive line graph of performance of user's 
	wealth invested in recommended allocation over past hist_period years
	using Python package plotly.

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

	# Get portfolio prices for proper hist_period and allocation
	pf_prices = c.execute("SELECT * FROM " + allocation + "_" + \
		TIME_DICT[hist_period] + "_Year_PF;")
	prices = pf_prices.fetchall()

	# Get dates in datetime format for label purposes
	date_list = [datetime.datetime.strptime(x[0], "%Y-%m-%d %H:%M:%S") \
		for x in prices]
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
	     title = 'Your Growth in Wealth Over Past 10 Years: ' + allocation, 
	     yaxis = dict(
	     	title = 'Your Portfolio Value ($)'),
	     xaxis = dict(
	     	title = 'Year')
	)

	fig = go.Figure(data = data, layout = layout)
	plot_url = py.plot(fig, filename = 'User-Portfolio-Performance', \
		auto_open = False)

	annualized_return = (((price_list[-1] / price_list[0]) ** \
		(1 / int(hist_period[:-1]))) - 1) * 100
	
	connection.commit()
	connection.close

	return str("{0:.2f}".format(annualized_return)) + "%"


def graph_worst_year_plotly(allocation, wealth, worst_year_start_date, worst_year_end_date, hist_period = '10y'):
	'''
	Modified from https://plot.ly/python/line-charts/

	Create interative line graph of person's decrease in wealth 
	over worst 12-month period over past hist_period years using Python 
	package plotly. 

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

	pf_prices = c.execute("SELECT * FROM " + allocation + "_" + \
		TIME_DICT[hist_period] + "_Year_PF WHERE Date >= '" + \
		worst_year_start_date + "' AND Date <= '" + worst_year_end_date + "';")
	prices = pf_prices.fetchall()

	# Get dates in datetime format
	date_list = [datetime.datetime.strptime(x[0], "%Y-%m-%d %H:%M:%S") \
		for x in prices]
	price_list = [(x[1] / prices[0][1]) * wealth for x in prices]

	data = [
	    go.Scatter(
	        x = date_list,
	        y = price_list,
	        line = dict(
	        	color = ('rgb(259, 0, 0)')
	        )
	    )
	]

	layout = go.Layout(
	     title = 'Worst 12-Month Performance Over Past 10 Years: ' + allocation, 
	     yaxis = dict(
	     	title = 'Your Portfolio Value ($)'),
	     xaxis = dict(
	     	title = 'Date')
	)

	fig = go.Figure(data = data, layout = layout)
	plot_url = py.plot(fig, filename = 'User-Worst-Year', auto_open = False)

	connection.commit()
	connection.close


def graph_best_year_plotly(allocation, wealth, best_year_start_date, best_year_end_date, hist_period = '10y'):
	'''
	Modified from https://plot.ly/python/line-charts/

	Function to create interative line graph of user's increase in wealth 
	over best 12-month period over past hist_period years using Python 
	package plotly. 

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

	# Get portfolio prices for proper hist_period and allocation
	pf_prices = c.execute("SELECT * FROM " + allocation + "_" + \
		TIME_DICT[hist_period] + "_Year_PF WHERE Date >= '" + \
		best_year_start_date + "' AND Date <= '" + best_year_end_date + "';")
	prices = pf_prices.fetchall()

	# Get dates in datetime format
	date_list = [datetime.datetime.strptime(x[0], "%Y-%m-%d %H:%M:%S") \
		for x in prices]
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
	     title = 'Best 12-Month Performance Over Past 10 Years: ' + allocation, 
	     yaxis = dict(
	     	title = 'Your Portfolio Value ($)'),
	     xaxis = dict(
	     	title = 'Date')
	)

	fig = go.Figure(data = data, layout = layout)
	plot_url = py.plot(fig, filename = 'User-Best-Year', auto_open = False)

	connection.commit()
	connection.close

