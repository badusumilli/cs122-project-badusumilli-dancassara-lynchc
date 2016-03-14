# Robo-advisor Project: Dan Cassara, Connor Lynch, Bobby Adusumilli

# This file contains functions to create tables in roboadvisor.db of 
# historical performance for each potential recommended portfolio. 

import sqlite3
import pandas
from pandas.io.data import DataReader
import datetime
import sys

TIME_DICT = {'1y': 'One', '5y': 'Five', '10y': 'Ten'}

# For calculating historical prices of recommended portfolios for 1, 5 years.
# Since Vanguard ETFs tend to be newer, their equivalent mutual funds have 
# longer historical pricing data, which we used when necessary
ALLOCATION_LIST = ['VNQI', 'VBR', 'VNQ', 'VTI', 'VEA', 'VGTSX', 'VSS', 'BND', \
	'BSV', 'VWO']

ALLOCATION_DICT = { 
	'Very_Conservative': {'VTI': 0.10, 'VBR': 0.02, 
	'VEA': 0.04, 'VWO': 0.01, 'VSS': 0.01, 'VNQ': 0.01, 'VNQI': 0.01,
	'BND': 0.48, 'BSV': 0.12, 'VGTSX': 0.20}, 
	'Conservative': {'VTI': 0.20, 'VBR': 0.04, 
	'VEA': 0.08, 'VWO': 0.02, 'VSS': 0.02, 'VNQ': 0.02, 'VNQI': 0.02,
	'BND': 0.36, 'BSV': 0.09, 'VGTSX': 0.15},
	'Balanced': {'VTI': 0.30, 'VBR': 0.06, 
	'VEA': 0.12, 'VWO': 0.03, 'VSS': 0.03, 'VNQ': 0.03, 'VNQI': 0.03,
	'BND': 0.24, 'BSV': 0.06, 'VGTSX': 0.10},
	'Aggressive': {'VTI': 0.40, 'VBR': 0.08, 
	'VEA': 0.16, 'VWO': 0.04, 'VSS': 0.04, 'VNQ': 0.04, 'VNQI': 0.04,
	'BND': 0.12, 'BSV': 0.03, 'VGTSX': 0.05},
	'Very_Aggressive': {'VTI': 0.50, 'VBR': 0.10, 
	'VEA': 0.20, 'VWO': 0.05, 'VSS': 0.05, 'VNQ': 0.05, 'VNQI': 0.05,
	'BND': 0.00, 'BSV': 0.00, 'VGTSX': 0.00}
}

# For calculating historical prices of recommended portfolios for 10 years.
# The ETFs VSS and VNQI did not have historical prices over 10 years, so we 
# had to slightly alter historical performance to account for this, 
# but the changes are not significant for overall portfolio returns
HISTORICAL_LIST = ['VBMFX', 'VBR', 'VNQ', 'VTI', 'VGTSX', 'VTMGX', 'VBISX', \
	'VWO']

HISTORICAL_DICT = {
	'Very_Conservative': {'VTI': 0.10, 'VBR': 0.02, 'VTMGX': 0.05, 
	'VWO': 0.01, 'VNQ': 0.02, 'VBMFX': 0.48, 'VBISX': 0.12, 'VGTSX': 0.20}, 
	'Conservative': {'VTI': 0.20, 'VBR': 0.04, 'VTMGX': 0.10, 
	'VWO': 0.02, 'VNQ': 0.04, 'VBMFX': 0.36, 'VBISX': 0.09, 'VGTSX': 0.15}, 
	'Balanced': {'VTI': 0.30, 'VBR': 0.06, 'VTMGX': 0.15, 
	'VWO': 0.03, 'VNQ': 0.06, 'VBMFX': 0.24, 'VBISX': 0.06, 'VGTSX': 0.10}, 
	'Aggressive': {'VTI': 0.40, 'VBR': 0.08, 'VTMGX': 0.20, 
	'VWO': 0.04, 'VNQ': 0.08, 'VBMFX': 0.12, 'VBISX': 0.03, 'VGTSX': 0.05}, 
	'Very_Aggressive': {'VTI': 0.50, 'VBR': 0.10, 'VTMGX': 0.25, 
	'VWO': 0.05, 'VNQ': 0.10, 'VBMFX': 0.00, 'VBISX': 0.00, 'VGTSX': 0.00}
}

# Because of limited 10 year data of ETFs, first 5 years based on certain 
# ETFs, while last 5 years based on all recommended ETFs / equivalent 
# mutual funds
CHOOSE_DICT = {
	'1y': ALLOCATION_DICT, 
	'5y': ALLOCATION_DICT, 
	'10y': HISTORICAL_DICT
}


def create_each_potential_portfolio():
	'''
	Original function.

	Function to create historical prices for each possible recommended 
	portfolio. This is updated daily through Cron.

	Outputs: 
		Updated sqlite3 price tables for 1, 5, and 10 year portfolios of 
			each possible recommended portfolio
	'''
	connection = sqlite3.connect("roboadvisor.db")
	c = connection.cursor()

	for years in CHOOSE_DICT.keys():
		create_table(years)
		for allocation in ALLOCATION_DICT.keys():
			get_historical_pf_prices(allocation, years)

	connection.commit()
	connection.close


def create_table(hist_period):
	'''
	Original function

	Create sqlite3 table with normalized historical prices of all Vanguard 
	ETFs / mutual funds over a given number of years (hist_period) that will 
	be used to calculate historical prices for each potential recommended 
	portfolio

	Input: 
		hist_period: string of years for historical portfolio prices 
			(ex: '10y')

	Outputs: 
		sqlite3 table(s) with normalized historical prices of all Vanguard 
			ETFs / mutual funds for given hist_period. For hist_period = '10y', 
			since not all Vanguard ETF / mutual fund data goes back 10 
			years, we are calculating return info through a manipulated
			process with the data we have. 
	'''
	connection = sqlite3.connect("roboadvisor.db")
	c = connection.cursor()

	hist_date = datetime.datetime.now().date()
	# Start date of relevant data
	hist_date_old = hist_date.replace(year = hist_date.year - \
		int(hist_period[:-1]))
	# for '10y' data. Gives middle 5 year date
	hist_date_new = hist_date.replace(year = hist_date.year - \
		int(hist_period[:-1]) + 5)

	if hist_period != '10y':
		c.execute("DROP TABLE IF EXISTS " + TIME_DICT[hist_period] + \
			"_Year_Prices")
		create_statement = "CREATE TABLE " + TIME_DICT[hist_period] + \
			"_Year_Prices ("

		create_statement, sql_query = create_sql_statements(ALLOCATION_LIST, \
			hist_period, hist_date_old, hist_date_new, create_statement)
		c.execute(create_statement)
		c.execute("INSERT INTO " + TIME_DICT[hist_period] + "_Year_Prices " + \
			sql_query)

	# Must combine datasets because of limited 10 year data. Use funds / ETFs
	# from HISTORICAL_LIST
	else: 
		c.execute("DROP TABLE IF EXISTS " + TIME_DICT[hist_period] + \
			"_Year_Prices_Old")
		create_statement_old = "CREATE TABLE " + TIME_DICT[hist_period] + \
			"_Year_Prices_Old ("

		create_statement_old, sql_query_old = create_sql_statements\
			(HISTORICAL_LIST, hist_period, hist_date_old, hist_date_new, \
			create_statement_old)
		c.execute(create_statement_old)
		c.execute("INSERT INTO " + TIME_DICT[hist_period] + \
			"_Year_Prices_Old " + sql_query_old)

		# Most recent 5 years with the recommended ETFs / funds from 
		# ALLOCATION_LIST
		c.execute("DROP TABLE IF EXISTS " + TIME_DICT[hist_period] + \
			"_Year_Prices_New")
		create_statement_new = "CREATE TABLE " + TIME_DICT[hist_period] + \
		"_Year_Prices_New ("
		create_statement_new, sql_query_new = create_sql_statements\
			(ALLOCATION_LIST, hist_period, hist_date_new, hist_date_new, \
			create_statement_new)
		c.execute(create_statement_new)
		c.execute("INSERT INTO " + TIME_DICT[hist_period] + \
			"_Year_Prices_New " + sql_query_new)

	connection.commit()
	connection.close


def create_sql_statements(fund_list, hist_period, hist_date_old, hist_date_new, create_statement):
	'''
	Original function

	Helper function to create_table that creates string of sqlite3 query 
	to create the relevant sqlite3 tables with all historical Vanguard ETFs / 
	mutual funds data over hist_period

	Inputs: 
		fund_list: list of Vanguard ETFs / mutual funds to find the  
			historical prices for (ex: ['VTI', 'BND'])
		hist_period: string of years for historical portfolio prices 
			(ex: '10y')
		hist_date_old: starting date (ex: datetime.date(2016, 3, 9)) to 
			calculate normalized value (over hist_period) of a given 
			ETF / fund 
		hist_date_new: ending date (ex: datetime.date(2016, 3, 9)) to 
			calculate normalized value (over hist_period) of a given 
			ETF / fund 
		create_statement: sqlite3 query string to create necessary table 
			with normalized historical prices of Vanguard ETFs / funds 
			over hist_period

	Outputs: 
		create_statement: updated sqlite3 query string to create necessary 
			table with normalized historical prices of Vanguard ETFs / funds 
			over hist_period
		sql_query: sqlite3 query string to add necessary normalized
			historical prices of Vanguard ETFs / funds over hist_period
			to the specified table
	'''
	select_statement = ""
	from_statement = ""
	join_statement = ""
	on_statement = ""
	where_statement = ""

	for fund in fund_list:
		# for first fund in list
		if where_statement == "":
			# Normalize the fund / ETF prices over the hist_period
			select_statement += "SELECT " + fund + ".Date, " + "(" + fund + \
				".Adj_Close / (SELECT Adj_Close FROM " + fund + \
				" WHERE Date >= '" + str(hist_date_old) + "' LIMIT 1)), "
			from_statement += "FROM " + fund + " "

			if fund_list != HISTORICAL_LIST: 
				where_statement += "WHERE " + fund + ".Date >= '" + \
					str(hist_date_old) + "' "

			# Only data from first 5 years of recent 10 year period
			else: 
				where_statement += "WHERE " + fund + ".Date >= '" + \
					str(hist_date_old) + "' AND " + fund + ".Date <= '" \
					+ str(hist_date_new) + "' "

			on_clause = fund + ".Date"
			create_statement += "Date TIMESTAMP, " + fund + "_Price REAL, "

		else: 
			select_statement += "(" + fund + ".Adj_Close / (SELECT Adj_Close FROM " \
				+ fund + " WHERE Date >= '" + str(hist_date_old) + "' LIMIT 1)), "
			join_statement += "JOIN " + fund + " "

			if on_statement == "":
				on_statement += "ON " + on_clause + " = " + fund + ".Date "

			else: 
				on_statement += "AND " + on_clause + " = " + fund + ".Date "
			create_statement += fund + "_Price REAL, "

	select_statement = select_statement[:-2] + " "
	where_statement = where_statement[:-1] + ";"
	sql_query = select_statement + from_statement + join_statement + \
		on_statement + where_statement

	create_statement = create_statement[:-2] + ");"

	return create_statement, sql_query


def get_historical_pf_prices(allocation, hist_period):
	'''
	Original function

	Function to calculate normalized historical prices of a potential 
	recommended portfolio (allocation) over a specified period (hist_period)

	Inputs: 
		allocation: specified allocation (ex. 'Aggressive') 
		hist_period: string of years for historical portfolio prices 
			(ex: '10y')

	Output: 
		allocation_Year_PF: sqlite3 table of normalized historical
		prices of an allocation over hist_period 
	'''
	connection = sqlite3.connect("roboadvisor.db")
	c = connection.cursor()

	dictionary = CHOOSE_DICT[hist_period]

	# Tables need to be updated every day for proper portfolio prices over 
	# hist_period and allow for proper portfolio rebalancing
	c.execute("DROP TABLE IF EXISTS " + allocation + "_" + \
		TIME_DICT[hist_period] + "_Year_PF")
	create_statement = "CREATE TABLE " + allocation + "_" + \
		TIME_DICT[hist_period] + "_Year_PF (Date TIMESTAMP, PF_Price REAL);"

	select_statement = "SELECT Date, ("

	for fund, weight in dictionary[allocation].items():
		select_statement += "(" + str(weight) + " * " + fund + "_Price) + "

	select_statement = select_statement[:-3] + ") "

	# 10 year data is limited, so must combine data from different funds
	if hist_period != '10y':
		from_statement = "FROM " + TIME_DICT[hist_period] + "_Year_Prices;"

	# 10 year data is limited, so must combine data from different funds
	else: 
		from_statement = "FROM " + TIME_DICT[hist_period] + "_Year_Prices_Old;"

	c.execute(create_statement)
	c.execute("INSERT INTO " + allocation + "_" + TIME_DICT[hist_period] + \
		"_Year_PF " + select_statement + from_statement)

	# Combining 10_Year_Prices_Old and 10_Year_Prices_New tables
	if hist_period == '10y':
		x = c.execute("SELECT * FROM " + allocation + "_" + \
			TIME_DICT[hist_period] + "_Year_PF ORDER BY Date DESC LIMIT 1;")
		results = x.fetchone()
		prev_date = results[0]
		pf_price = results[1]

		select_statement = "SELECT Date, (" + str(pf_price) + " * ("

		for fund, weight in ALLOCATION_DICT[allocation].items():
			select_statement += "(" + str(weight) + " * " + fund + "_Price) + "

		select_statement = select_statement[:-3] + ")) "

		from_statement = "FROM " + TIME_DICT[hist_period] + \
			"_Year_Prices_New WHERE Date > '" + prev_date + "';"
		c.execute("INSERT INTO " + allocation + "_" + TIME_DICT[hist_period] \
			+ "_Year_PF " + select_statement + from_statement)

	connection.commit()
	connection.close


def find_worst_and_best_year(allocation, hist_period = '10y'):
	'''
	Original function

	Function to find worst 12-month and best 12-month performances
	of a specific allocation over the specified hist_period

	Inputs: 
		allocation: specified allocation (ex. 'Aggressive') 
		hist_period: string of years for historical portfolio prices 
			(ex: '10y')

	Outputs: 
		worst_year_change: String of percentage (ex: '-1.83%') of loss
			in portfolio value over worst 12-month period
		worst_year_start_date: Start date of worst 12-month period
		worst_year_end_date: End date of worst 12-month period
		best_year_change: String of percentage (ex: '1.83%') of gain
			in portfolio value over best 12-month period
		best_year_start_date: Start date of best 12-month period
		best_year_end_date: End date of best 12-month period
	'''
	connection = sqlite3.connect("roboadvisor.db")
	c = connection.cursor()

	pf_prices = c.execute("SELECT * FROM " + allocation + "_" + \
		TIME_DICT[hist_period] + "_Year_PF;")
	prices = pf_prices.fetchall()

	# Get dates in datetime format for querying purposes
	date_list = [datetime.datetime.strptime(x[0], "%Y-%m-%d %H:%M:%S") \
		for x in prices]
	price_list = [x[1] for x in prices]

	worst_year_start_date = ''
	worst_year_end_date = ''
	worst_year_change = 0

	best_year_start_date = ''
	best_year_end_date = ''
	best_year_change = 0

	# Don't need to check dates within the past year
	for date in range(len(date_list) - 251):

		next_year_date = date_list[date] + datetime.timedelta(days = 365)
		next_year_date = next_year_date.strftime("%Y-%m-%d %H:%M:%S")
		next_year_price = c.execute("SELECT PF_Price FROM " + allocation + "_" \
			+ TIME_DICT[hist_period] + "_Year_PF WHERE Date < '" + \
			next_year_date + "' ORDER BY Date DESC LIMIT 1;")
		next_price = next_year_price.fetchone()[0]
		
		# In case next_price yields no price
		if next_price != []: 
			price_change = ((next_price - price_list[date]) / \
				price_list[date]) * 100

			if price_change < worst_year_change: 
				worst_year_change = price_change
				worst_year_start_date = \
					date_list[date].strftime("%Y-%m-%d %H:%M:%S")
				worst_year_end_date = next_year_date

			if price_change > best_year_change: 
				best_year_change = price_change
				best_year_start_date = \
					date_list[date].strftime("%Y-%m-%d %H:%M:%S")
				best_year_end_date = next_year_date

	worst_year_change = str("{0:.2f}".format(worst_year_change)) + "%"
	best_year_change = str("{0:.2f}".format(best_year_change)) + "%"

	connection.commit()
	connection.close

	return worst_year_change, worst_year_start_date, worst_year_end_date, \
		best_year_change, best_year_start_date, best_year_end_date


def create_table_worst_best_years():
	'''
	Original function

	Create table in roboadvisor.db with dates and percentage changes of 
	worst and best 12-month periods for each potential recommended portfolio 
	over the past 10 years

	Output: 
		Best_Worst_Year: Table in roboadvisor.db with dates and portfolio 
			price changes of worst and best 12-month periods over past 10 
			years for each allocation
	'''
	connection = sqlite3.connect("roboadvisor.db")
	c = connection.cursor()
	c.execute("DROP TABLE IF EXISTS Best_Worst_Year;")
	c.execute("CREATE TABLE Best_Worst_Year (Allocation REAL, Worst_Change " \
		+ "REAL, Worst_Start_Date REAL, Worst_End_Date REAL, Best_Change REAL, " \
		+ "Best_Start_Date REAL, Best_End_Date REAL);")

	for allocation in ALLOCATION_DICT.keys():
		worst_year_change, worst_year_start_date, worst_year_end_date, \
			best_year_change, best_year_start_date, best_year_end_date = \
		find_worst_and_best_year(allocation)
		c.execute("INSERT INTO Best_Worst_Year VALUES ('" + allocation + "', '" \
			+ worst_year_change + "', '" + worst_year_start_date + "', '" \
			+ worst_year_end_date + "', '" + best_year_change + "', '" \
			+ best_year_start_date + "', '" + best_year_end_date + "')")

	connection.commit()
	connection.close


#######################################################################################333
if __name__=="__main__":
	num_args = len(sys.argv)

	#run the two functions
	create_each_potential_portfolio()
	create_table_worst_best_years() 