import datetime
import sqlite3
import numpy as np
import matplotlib.pyplot as plt

TIME_DICT = {'1y': 'One', '5y': 'Five', '10y': 'Ten'}

ALLOCATION_LIST = ['VSS', 'VNQ', 'VTI', 'BND', 'VNQI', 'VWO', 'BSV', 'VBR', 'VEA', 'VGTSX']
HISTORICAL_LIST = ['VNQ', 'VBMFX', 'VTI', 'VTMGX', 'VBISX', 'VWO', 'VBR', 'VGTSX']

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

CHOOSE_DICT = {
	'1y': ALLOCATION_DICT, 
	'5y': ALLOCATION_DICT, 
	'10y': HISTORICAL_DICT
}


def create_potential_portfolios():
	for years in CHOOSE_DICT.keys():
		create_table(years)


def create_each_portfolio():
	for years in CHOOSE_DICT.keys():
		for allocation in ALLOCATION_DICT.keys():
			get_historical_pf_prices(allocation, years)


def create_table(hist_period):

	connection = sqlite3.connect("roboadvisor.db")
	c = connection.cursor()

	hist_date = datetime.datetime.now().date()
	hist_date_old = hist_date.replace(year = hist_date.year - int(hist_period[:-1]))
	hist_date_new = hist_date.replace(year = hist_date.year - int(hist_period[:-1]) + 5)

	if hist_period != '10y':
		c.execute("DROP TABLE IF EXISTS " + TIME_DICT[hist_period] + "_Year_Prices")
		create_statement = "CREATE TABLE " + TIME_DICT[hist_period] + "_Year_Prices ("
		create_statement, sql_query = create_sql_statements(ALLOCATION_LIST, hist_period, hist_date_old, hist_date_new, create_statement)
		c.execute(create_statement)
		c.execute("INSERT INTO " + TIME_DICT[hist_period] + "_Year_Prices " + sql_query)

	else: 
		c.execute("DROP TABLE IF EXISTS " + TIME_DICT[hist_period] + "_Year_Prices_Old")
		create_statement_old = "CREATE TABLE " + TIME_DICT[hist_period] + "_Year_Prices_Old ("
		create_statement_old, sql_query_old = create_sql_statements(HISTORICAL_LIST, hist_period, hist_date_old, hist_date_new, create_statement_old)
		c.execute(create_statement_old)
		c.execute("INSERT INTO " + TIME_DICT[hist_period] + "_Year_Prices_Old " + sql_query_old)

		c.execute("DROP TABLE IF EXISTS " + TIME_DICT[hist_period] + "_Year_Prices_New")
		create_statement_new = "CREATE TABLE " + TIME_DICT[hist_period] + "_Year_Prices_New ("
		create_statement_new, sql_query_new = create_sql_statements(ALLOCATION_LIST, hist_period, hist_date_new, hist_date_new, create_statement_new)
		c.execute(create_statement_new)
		c.execute("INSERT INTO " + TIME_DICT[hist_period] + "_Year_Prices_New " + sql_query_new)

	connection.commit()
	connection.close


def create_sql_statements(fund_list, hist_period, hist_date_old, hist_date_new, create_statement):
	select_statement = ""
	from_statement = ""
	join_statement = ""
	on_statement = ""
	where_statement = ""

	for fund in fund_list:
		if where_statement == "":
			select_statement += "SELECT " + fund + ".Date, " + "(" + fund + ".Adj_Close / (SELECT Adj_Close FROM " + fund + " WHERE Date >= '" + str(hist_date_old) + "' LIMIT 1)), "
			from_statement += "FROM " + fund + " "

			if fund_list != HISTORICAL_LIST: 
				where_statement += "WHERE " + fund + ".Date >= '" + str(hist_date_old) + "' "
			else: 
				where_statement += "WHERE " + fund + ".Date >= '" + str(hist_date_old) + "' AND " + fund + ".Date <= '" + str(hist_date_new) + "' "

			on_clause = fund + ".Date"
			create_statement += "Date TIMESTAMP, " + fund + "_Price REAL, "

		else: 
			select_statement += "(" + fund + ".Adj_Close / (SELECT Adj_Close FROM " + fund + " WHERE Date >= '" + str(hist_date_old) + "' LIMIT 1)), "
			join_statement += "JOIN " + fund + " "
			if on_statement == "":
				on_statement += "ON " + on_clause + " = " + fund + ".Date "
			else: 
				on_statement += "AND " + on_clause + " = " + fund + ".Date "
			create_statement += fund + "_Price REAL, "

	select_statement = select_statement[:-2] + " "
	where_statement = where_statement[:-1] + ";"
	sql_query = select_statement + from_statement + join_statement + on_statement + where_statement

	create_statement = create_statement[:-2] + ");"

	return create_statement, sql_query


def get_historical_pf_prices(allocation, hist_period):

	connection = sqlite3.connect("roboadvisor.db")
	c = connection.cursor()

	dictionary = CHOOSE_DICT[hist_period]

	c.execute("DROP TABLE IF EXISTS " + allocation + "_" + TIME_DICT[hist_period] + "_Year_PF")
	create_statement = "CREATE TABLE " + allocation + "_" + TIME_DICT[hist_period] + "_Year_PF (Date TIMESTAMP, PF_Price REAL);"

	select_statement = "SELECT Date, ("

	for fund, weight in dictionary[allocation].items():
		select_statement += "(" + str(weight) + " * " + fund + "_Price) + "

	select_statement = select_statement[:-3] + ") "

	if hist_period != '10y':
		from_statement = "FROM " + TIME_DICT[hist_period] + "_Year_Prices;"
	else: 
		from_statement = "FROM " + TIME_DICT[hist_period] + "_Year_Prices_Old;"

	c.execute(create_statement)
	c.execute("INSERT INTO " + allocation + "_" + TIME_DICT[hist_period] + "_Year_PF " + select_statement + from_statement)

	if hist_period == '10y':
		x = c.execute("SELECT * FROM " + allocation + "_" + TIME_DICT[hist_period] + "_Year_PF ORDER BY Date DESC LIMIT 1;")
		results = x.fetchone()
		prev_date = results[0]
		pf_price = results[1]

		select_statement = "SELECT Date, (" + str(pf_price) + " * ("

		for fund, weight in ALLOCATION_DICT[allocation].items():
			select_statement += "(" + str(weight) + " * " + fund + "_Price) + "

		select_statement = select_statement[:-3] + ")) "

		from_statement = "FROM " + TIME_DICT[hist_period] + "_Year_Prices_New WHERE Date > '" + prev_date + "';"
		c.execute("INSERT INTO " + allocation + "_" + TIME_DICT[hist_period] + "_Year_PF " + select_statement + from_statement)

	connection.commit()
	connection.close


def allocation_bar(allocation, save_to = None):
	# http://matplotlib.org/examples/api/barchart_demo.html
	# http://matplotlib.org/examples/pylab_examples/barchart_demo.html
	funds = list(ETF_ALLOCATION_DICT[allocation].keys())
	percentages = [x * 100 for x in ETF_ALLOCATION_DICT[allocation].values()]

	width = 0.35
	y_pos = np.arange(len(funds))

	# fig = plt.figure(figsize = (8,8)) 
	fig, ax = plt.subplots()
	# colors: http://matplotlib.org/examples/color/named_colors.html
	rects = ax.barh(y_pos, percentages, 0.65, align='center', color = 'skyblue')
	ax.set_xlabel('Portfolio Percentage (%)')
	ax.set_yticks(y_pos)
	ax.set_yticklabels(funds)
	ax.set_title('Your Portfolio Allocation')

	for rect in rects: 
		ax.text(rect.get_width() + 0.40, rect.get_y() + rect.get_height()/4., rect.get_width())

	# plt.tight_layout()
	if save_to is None: 
		plt.show()
	else: 
		fig.savefig(save_to)


def fund_performance_graph(allocation, hist_period, wealth):
	connection = sqlite3.connect("roboadvisor.db")
	c = connection.cursor()

	pf_prices = c.execute("SELECT * FROM " + allocation + "_" + TIME_DICT[hist_period] + "_Year_PF;")
	prices = pf_prices.fetchall()
	date_list = [x[0] for x in prices]
	price_list = [x[1] * wealth for x in prices]
	y_pos = np.arange(len(date_list))

	fig, ax = plt.subplots()
	rects = ax.bar(y_pos, price_list, 0.65, align='center', color = 'blue')

	plt.show()





