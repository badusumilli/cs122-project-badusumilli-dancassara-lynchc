import datetime
import sqlite3

TIME_DICT = {'1y': 'One', '5y': 'Five', '10y': 'Ten'}

ALLOCATION_DICT = { 'Very Conservative': {'VTI': 0.10, 'VBR': 0.02, 
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
'Very Aggressive': {'VTI': 0.50, 'VBR': 0.10, 
'VEA': 0.20, 'VWO': 0.05, 'VSS': 0.05, 'VNQ': 0.05, 'VNQI': 0.05,
'BND': 0.0, 'BSV': 0.0, 'VGTSX': 0.0}
}


ETF_ALLOCATION_DICT = { 'Very Conservative': {'VTI': 0.10, 'VBR': 0.02, 
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
'Very Aggressive': {'VTI': 0.50, 'VBR': 0.10, 
'VEA': 0.20, 'VWO': 0.05, 'VSS': 0.05, 'VNQ': 0.05, 'VNQI': 0.05,
'BND': 0.0, 'BSV': 0.0, 'BNDX': 0.0}
}



HISTORICAL_DICT = {
	'Very Conservative': {'VTI': 0.10, 'VBR': 0.02, 'VTMGX': 0.05, 
	'VWO': 0.01, 'VNQ': 0.02, 'VBMFX': 0.48, 'VBISX': 0.12, 'VGTSX': 0.20}, 
	'Conservative': {'VTI': 0.20, 'VBR': 0.04, 'VTMGX': 0.10, 
	'VWO': 0.02, 'VNQ': 0.04, 'VBMFX': 0.36, 'VBISX': 0.09, 'VGTSX': 0.15}, 
	'Balanced': {'VTI': 0.30, 'VBR': 0.06, 'VTMGX': 0.15, 
	'VWO': 0.03, 'VNQ': 0.06, 'VBMFX': 0.24, 'VBISX': 0.06, 'VGTSX': 0.10}, 
	'Aggressive': {'VTI': 0.40, 'VBR': 0.08, 'VTMGX': 0.20, 
	'VWO': 0.04, 'VNQ': 0.08, 'VBMFX': 0.12, 'VBISX': 0.03, 'VGTSX': 0.05}, 
	'Very Aggressive': {'VTI': 0.50, 'VBR': 0.10, 'VTMGX': 0.25, 
	'VWO': 0.05, 'VNQ': 0.10, 'VBMFX': 0.00, 'VBISX': 0.00, 'VGTSX': 0.00}
}

CHOOSE_DICT = {
	'1y': ALLOCATION_DICT, 
	'5y': ALLOCATION_DICT, 
	'10y': HISTORICAL_DICT
}

def create_table(allocation, hist_period):

	connection = sqlite3.connect("roboadvisor.db")
	c = connection.cursor()

	dictionary = CHOOSE_DICT[hist_period]

	hist_date = datetime.datetime.now().date()
	hist_date = hist_date.replace(year = hist_date.year - int(hist_period[:-1]))

	select_statement = ""
	from_statement = ""
	join_statement = ""
	on_statement = ""
	where_statement = ""

	c.execute("DROP TABLE IF EXISTS " + TIME_DICT[hist_period] + "_Year_Prices")

	create_statement = "CREATE TABLE " + TIME_DICT[hist_period] + "_Year_Prices ("

	for fund in dictionary[allocation].keys():
		if where_statement == "":
			select_statement += "SELECT " + fund + ".Date, " + "(" + fund + ".Adj_Close / (SELECT Adj_Close FROM " + fund + " WHERE Date >= '" + str(hist_date) + "' LIMIT 1)), "
			from_statement += "FROM " + fund + " "
			where_statement += "WHERE " + fund + ".Date >= '" + str(hist_date) + "' "
			on_clause = fund + ".Date"
			create_statement += "Date TIMESTAMP, " + fund + "_Price REAL, "

		else: 
			select_statement += "(" + fund + ".Adj_Close / (SELECT Adj_Close FROM " + fund + " WHERE Date >= '" + str(hist_date) + "' LIMIT 1)), "
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

	c.execute(create_statement)
	c.execute("INSERT INTO " + TIME_DICT[hist_period] + "_Year_Prices " + sql_query)

	connection.commit()
	connection.close

def get_historical_pf_prices(allocation, hist_period):

	connection = sqlite3.connect("roboadvisor.db")
	c = connection.cursor()

	dictionary = CHOOSE_DICT[hist_period]

	c.execute("DROP TABLE IF EXISTS " + allocation + "_" + TIME_DICT[hist_period] + "_Year_PF_Prices")

	create_statement = "CREATE TABLE " + allocation + "_" + TIME_DICT[hist_period] + "_Year_PF_Prices (Date TIMESTAMP, PF_Price REAL);"

	select_statement = "SELECT Date, ("

	for fund, weight in dictionary[allocation].items():
		select_statement += "(" + str(weight) + " * " + fund + "_Price) + "

	select_statement = select_statement[:-3] + ") "

	from_statement = "FROM " + TIME_DICT[hist_period] + "_Year_Prices;"

	c.execute(create_statement)
	c.execute("INSERT INTO " + allocation + "_" + TIME_DICT[hist_period] + "_Year_PF_Prices " + select_statement + from_statement)

	connection.commit()
	connection.close


