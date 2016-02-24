#Query our SQL database and get real return information for a fund

import sqlite3
import datetime

#day = datetime.datetime.strptime(date, '%B %d, %Y').strftime('%A')
TIME_DICT = { '1d': '1', '5d': '5', '3m': '66', '6m': '132', '1y': '252',
				'5y': '1260'    }

def calc_return_of_portfolio(allocation, time_frame):

	#given allocation, figure out what percent of each fund is in the allocation
	allocation_dict = { 'Very Conservative': {'VTI': 0.10, 'VBR': 0.02, 
	'VEA': 0.04, 'VWO': 0.01, 'VSS': 0.01, 'VNQ': 0.01, 'VNQI': 0.01,
	'BND': 0.48, 'VTIP': 0.12, 'BNDX': 0.20}, 
	'Conservative': {'VTI': 0.20, 'VBR': 0.04, 
	'VEA': 0.08, 'VWO': 0.02, 'VSS': 0.02, 'VNQ': 0.02, 'VNQI': 0.02,
	'BND': 0.36, 'VTIP': 0.09, 'BNDX': 0.15},
	'Balanced': {'VTI': 0.30, 'VBR': 0.06, 
	'VEA': 0.12, 'VWO': 0.03, 'VSS': 0.03, 'VNQ': 0.03, 'VNQI': 0.03,
	'BND': 0.24, 'VTIP': 0.06, 'BNDX': 0.10},
	'Aggressive': {'VTI': 0.40, 'VBR': 0.08, 
	'VEA': 0.16, 'VWO': 0.04, 'VSS': 0.04, 'VNQ': 0.04, 'VNQI': 0.04,
	'BND': 0.12, 'VTIP': 0.03, 'BNDX': 0.05},
	'Very Aggressive': {'VTI': 0.50, 'VBR': 0.10, 
	'VEA': 0.20, 'VWO': 0.05, 'VSS': 0.05, 'VNQ': 0.05, 'VNQI': 0.05,
	'BND': 0.0, 'VTIP': 0.0, 'BNDX': 0.0}
	}
	allocation_weights = allocation_dict[allocation]

	portfolio_return = 0.0
	#get return information for each fund		
	#take weighted avg to get return for the entire allocation
	for ticker, weight in allocation_weights.items():
		fund_return = get_return_data(ticker, time_frame)
		weighted_return = float(fund_return) * float(weight)

		portfolio_return += weighted_return

	return "{:.2%}".format(portfolio_return)

def get_return_data(ticker, time_frame):

	price_query = get_price_data(ticker, time_frame)

	prev_price = price_query[0][1]
	current_price = price_query[1][1]

	real_return = ( ( current_price / prev_price ) - 1 ) 
	return "{:.3f}".format(real_return)


def get_price_data(ticker, time_frame):

	dates = get_dates(ticker, time_frame)

	sql_query = "SELECT Date, Adj_Close FROM " + ticker + " WHERE Date in " + dates + " ; "
	# sql_inputs = ["('2016-02-05 00:00:00', '2016-02-03 00:00:00')"]
	sql_inputs = []

	connection = sqlite3.connect("roboadvisor.db")
	c = connection.cursor()
	output = c.execute(sql_query, sql_inputs)
	results = output.fetchall()
	connection.close

	return results

def create_query(ticker, dates):

	selection = "SELECT Date, Adj_Close"

	from_clause = "FROM " + ticker

	where = "WHERE Date in " + dates


def get_dates(ticker, time_frame):

	limit = TIME_DICT[time_frame]

	query = "SELECT Date FROM " + ticker + " ORDER BY Date DESC LIMIT " + limit + " ;"
	inputs = []

	connection = sqlite3.connect("roboadvisor.db")
	c = connection.cursor()
	output = c.execute(query, inputs)
	results = output.fetchall()
	connection.close


	num = len(results) - 1
	current_date = results[0][0]
	prev_date = results[num][0]

	return "('" + current_date + "', '" + prev_date + "')"




