cs122-project-badusumilli-dancassara-lynchc
Robo-Investment Advisor Project for CS122 WIN 2016

URL for github repository: 
https://github.com/badusumilli/cs122-project-badusumilli-dancassara-lynchc/

*** Graders need to install python package Plotly. Can use below command: 
pip3 install --user plotly


INSTRUCTIONS FOR RUNNING CODE:
In order to start the server and access the wesbsite, run
"python3 manage.py runserver" in the terminal from the folder
cs122-project-badusumilli-dancassara-lynchc/robo_ui


DOCUMENTATION OF CODE OWNERSHIP: 
"Direct copy" = From installed pacakge / website (ex. Stack Exchange) and
	few edits made

"Modified" = From installed package / website and meaningful edits made OR 
	heavily utilized template(s) provided by tutorial sessions

"Original" = Original code or heavily modified given structure





NEW TECHNOLOGIES USED: 

Pandas: Used to automatically download investment data from Yahoo Finance

Django: Used to create web interface

Plotly: Used to create interactive graphs based on user's recommended 
investment allocation

Cron: Automatically updates investment data everyday in sqlite3





FILES: 

Robo-Advisor-Initial-Plan.pdf: Initial proposal for Robo-Advisor project

bash_script_run_all.sh: bash / cron text to automatically update the 
investments / portfolio data in cs122-project-badusumilli-dancassara-lynchc/
robo_ui/quiz/roboadvisor.db

robo_ui: folder containing remaining relevant files for robo-advisor

robo_ui/quiz: folder containing files and functions that are necessary 
for running the quiz/using the survey

robo_ui/quiz/survey.py: takes a user's responses to the online quiz 
and returns a classification (suggested allocation)

robo_ui/quiz/roboadvisor.db: sqlite3 database with all relevant historical 
pricing data for the investments / portfolios

robo_ui/quiz/get_data.py: Contains functions to obtain historical investment 
data from Yahoo Finance and store this data into the sqlite3 database
roboadvisor.db

robo_ui/quiz/data.py: Contains functions to create portfolio prices and other 
necessary info for each possible allocation over past 1, 5, and 10 years 

robo_ui/quiz/portfolio_return.py: contains functions to create sqlite3 tables 
of historical pricing and performance data for each potential investment 
allocation. Also contains functions that create the historical 
performance graphs using the Python package Plotly

