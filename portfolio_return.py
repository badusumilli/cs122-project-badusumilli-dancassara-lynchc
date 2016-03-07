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

	# plt.tight_layout()
	if save_to is None: 
		plt.show()
	else: 
		fig.savefig(save_to)


def fund_performance_graph(allocation, hist_period, wealth, save_to = None):
	connection = sqlite3.connect("roboadvisor.db")
	c = connection.cursor()

	pf_prices = c.execute("SELECT * FROM " + allocation + "_" + TIME_DICT[hist_period] + "_Year_PF;")
	prices = pf_prices.fetchall()
	date_list = [datetime.datetime.strptime(x[0], "%Y-%m-%d %H:%M:%S") for x in prices]
	price_list = [x[1] * wealth for x in prices]
	x_pos = np.arange(len(date_list))

	fig = plt.figure(figsize = (8,8))
	ax = fig.add_axes([0.1, 0.2, 0.85, 0.75])

	ax.plot(date_list, price_list, color = 'skyblue')
	ax.fill_between(date_list, price_list, facecolor='skyblue', alpha = 0.5, lw=0.5)

	ax.set_ylim(min(price_list) - (wealth // 10), max(price_list) + (wealth // 10))
	ax.set_xlabel('Year')
	ax.set_ylabel('Portfolio Value ($)')
	ax.set_title(allocation + " Past " + hist_period[:-1] + "-Year Portfolio Performance")

	ax.text(1000, 2500, 'Value After 10 Years: ' + str(price_list[-1]), fontsize=10)

	if save_to is None: 
		plt.show()
	else: 
		fig.savefig(save_to)

def find_worst_year(allocation, hist_period):
	connection = sqlite3.connect("roboadvisor.db")
	c = connection.cursor()

	pf_prices = c.execute("SELECT * FROM " + allocation + "_" + TIME_DICT[hist_period] + "_Year_PF;")
	prices = pf_prices.fetchall()
	date_list = [datetime.datetime.strptime(x[0], "%Y-%m-%d %H:%M:%S") for x in prices]
	price_list = [x[1] for x in prices]

	worst_year_start_date = ''
	worst_year_end_date = ''
	worst_year_change = 0

	for date in range(len(date_list) - 251):

		next_year_date = date_list[date] + datetime.timedelta(days = 365)
		next_year_date = next_year_date.strftime("%Y-%m-%d %H:%M:%S")
		next_year_price = c.execute("SELECT PF_Price FROM " + allocation + "_" + TIME_DICT[hist_period] + "_Year_PF WHERE Date < '" + next_year_date + "' ORDER BY Date DESC LIMIT 1;")
		next_price = next_year_price.fetchone()[0]
		
		if next_price != []: 
			price_change = (next_price - price_list[date]) / price_list[date]
			if price_change < worst_year_change: 
				worst_year_change = price_change
				worst_year_start_date = date_list[date].strftime("%Y-%m-%d %H:%M:%S")
				worst_year_end_date = next_year_date

	return worst_year_change, worst_year_start_date, worst_year_end_date

def graph_worst_year(allocation, hist_period, wealth, save_to = None):
	connection = sqlite3.connect("roboadvisor.db")
	c = connection.cursor()

	worst_year_change, worst_year_start_date, worst_year_end_date = find_worst_year(allocation, hist_period)
	pf_prices = c.execute("SELECT * FROM " + allocation + "_" + TIME_DICT[hist_period] + "_Year_PF WHERE Date >= '" + worst_year_start_date + "' AND Date <= '" + worst_year_end_date + "';")
	prices = pf_prices.fetchall()
	date_list = [datetime.datetime.strptime(x[0], "%Y-%m-%d %H:%M:%S") for x in prices]
	price_list = [(x[1] / prices[0][1]) * wealth for x in prices]
	x_pos = np.arange(len(date_list))

	fig = plt.figure(figsize = (8,8))
	ax = fig.add_axes([0.1, 0.2, 0.85, 0.75])

	ax.plot(date_list, price_list, color = 'red')
	ax.fill_between(date_list, price_list, facecolor='red', alpha = 0.5, lw=0.5)


	ax.set_ylim(min(price_list) - (wealth // 10), max(price_list) + (wealth // 10))
	ax.set_xlabel('Year')
	ax.set_ylabel('Portfolio Value ($)')
	ax.set_title(allocation + " Worst 12 Month Portfolio Performance")
	for tick in ax.get_xticklabels():
		tick.set_rotation(90)

	# ax.text(1000, 2500, 'Value After 10 Years: ' + str(price_list[-1]), fontsize=10)

	if save_to is None: 
		plt.show()
	else: 
		fig.savefig(save_to)