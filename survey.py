#Create basic survey output

risk_score = 0
#####DEMOGRAPHIC QUESTIONS
q1 = input('How old are you?: ')
if q1 <= 55:
	if q1 <= 45:
		if q1 <= 30:
			score += 5
		elif q1 > 30:
			score += 3.5
	elif q1 > 45:
		score += 2

q2 = input('At what age do you plan to retire?: ')


print('Options: Single, Married, Other')
q3 = input('What is your marital status?: ')
	#Options: Single, Married, Divorced
	
if q3 == 'Single':
	score += 5
elif q3 == 'Married':
	score += 2
else: 
	pass

q4 = input('What is your annual income?: ')
print('Options: Strongly agree, somewhat agree, neutral, somewhat disagree, strongly disagree')

q5 = input('My current and future income sources are very stable: ')
	#Options: Strongly agree, somewhat agree, neutral, somewhat disagree, strongly disagree	

####BEHAVIORAL QUESTIONS
print('Options: Generating income, Growing wealth, Other')
q6 = input('What is your main goal in investing?: ')
	#Options: Generating income, Growing wealth, Other 
	#Options: Savings, Retirement, Other
print('Options: maximizing, minimizing, both equally')

q7 = input('Which is more important to you: Maximizing gains or mimimizing loses?: ')
	#Options: maximizing, minimizing, both equally
print('Options: A few months, 1-3 years, 3-5 Years, 5-10 Years, More than 10 years ')

q8 = input('I plan to begin using money from my investments in ___ years: ')
	#Options: A few months, 1-3 years, 3-5 Years, 5-10 Years, More than 10 years 
print('Options: 1000, 5000, 100000')

q9 = input('You are on a game show and given the choice between receiving $1000, \
	a 50% chance to win $5,000, or a 5% chance to win $100,000. Which do you pick?: ')
	#Options: 1000, 5000, 100000
print('Options: Sell everything, Sell some stocks, Do nothing, Buy more stocks')

q10 = input('The stock market drops 10% over the course of one month. What do you do?: ')
	#Options: Sell everything, Sell some stocks, Do nothing, Buy more stocks
