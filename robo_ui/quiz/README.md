README.md

roboadvisor.db: sqlite3 database with all relevant historical pricing
data for the investments / portfolios

data.py: Contains functions to obtain historical investment data 
from Yahoo Finance and store this data into the sqlite3 database
roboadvisor.db

portfolio_return.py: contains functions to create sqlite3 tables of 
historical pricing and performance data for each potential investment 
allocation. Also contains functions that create the historical 
performance graphs using the Python package Plotly