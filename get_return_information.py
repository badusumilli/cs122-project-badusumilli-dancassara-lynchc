#Query our SQL database and get real return information for a fund

import sqlite3
import datetime

#day = datetime.datetime.strptime(date, '%B %d, %Y').strftime('%A')
TIME_DICT = { '1d': '1', '5d': '5', '3m': '66', '6m': '132', '1y': '252',
				'5y': '1260'    }

def get_return_data(ticker, time_frame):

	price_query = get_price_data(ticker, time_frame)

	prev_price = price_query[0][1]
	current_price = price_query[1][1]

	real_return = ( ( current_price / prev_price ) - 1 ) / 100
	return "{:.2%}".format(real_return)


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




