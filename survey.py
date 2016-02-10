#Create basic survey output


def risk_tolerance():

	score = 0
	#####DEMOGRAPHIC QUESTIONS
	q1 = input('How old are you?: ')
	if int(q1) <= 55:
		if int(q1) <= 45:
			if int(q1) <= 30:
				score += 5
			elif int(q1) > 30:
				score += 3.5
		elif int(q1) > 45:
			score += 2

	print()
	q2 = input('At what age do you plan to retire?: ')

	print()
	print('Options: Single, Married, Other')
	q3 = input('What is your marital status?: ')
		#Options: Single, Married, Divorced
		
	if q3.lower() == 'single':
		score += 5
	elif q3.lower() == 'married':
		score += 2
	else: 
		pass

	print()
	q4 = input('What is your annual income?: ')
	if int(q4) >= 50000:
		if int(q4) >= 75000:
			if int(q4) >= 100000:
				score += 5
			else:
				score += 3.5
		else:
			score += 2

	print()
	print('Options: Strongly agree, somewhat agree, neutral, somewhat disagree, strongly disagree')
	q5 = input('My current and future income sources are very stable: ')
		#Options: Strongly agree, somewhat agree, neutral, somewhat disagree, strongly disagree	
	if q5.lower() == "strongly agree":
		score += 5
	elif q5.lower() == "somewhat agree":
		score += 4
	elif q5.lower() == "neutral":
		score += 2
	elif q5.lower() == "somewhat disagree":
		score += 1
	else:
		pass

	####BEHAVIORAL QUESTIONS
	print()
	print('Options: Generating income, Growing wealth, Other')
	q6 = input('What is your main goal in investing?: ')
		#Options: Generating income, Growing wealth, Other 
		#Options: Savings, Retirement, Other
	if q6.lower() == 'generating income':
		score += 2.5
	elif q6.lower() == 'growing wealth':
		score += 5
	else:
		pass

	print()
	print('Options: maximizing gains, minimizing loses, both equally')
	q7 = input('Which is more important to you: Maximizing gains or mimimizing loses?: ')
		#Options: maximizing, minimizing, both equally
	if q7.lower() == 'maximizing gains':
		score += 5
	elif q7.lower() == 'minimizing loses':
		score += 1
	elif q7.lower() == 'both equally':
		score += 3
	else:
		print('not an option')

	print()
	print('Options: A few months, 1-3 years, 3-5 Years, 5-10 Years, More than 10 years ')
	q8 = input('I plan to begin using money from my investments in ___ years: ')
		#Options: A few months, 1-3 years, 3-5 Years, 5-10 Years, More than 10 years 
	if q8.lower() == 'a few months':
		score += 1
	elif q8.lower() == '1-3 years':
		score += 2
	elif q8.lower() == '3-5 years':
		score += 3
	elif q8.lower() == '5-10 years':
		score += 4
	elif q8.lower() == 'more than 10 years':
		score += 5
	else:
		print('not an option')

	print()
	print('Options: 1000, 5000, 100000')
	q9 = input('You are on a game show and given the choice between receiving $1000, \
		a 50% chance to win $5,000, or a 5% chance to win $100,000. Which do you pick?: ')
		#Options: 1000, 5000, 100000
	if q9 == '1000':
		score += 1
	elif q9 == '5000':
		score += 3
	elif q9 == '100000':
		score += 5
	else:
		print('not an option')

	print()
	print('Options: Sell everything, Sell some stocks, Do nothing, Buy more stocks')
	q10 = input('The stock market drops 10% over the course of one month. What do you do?: ')
		#Options: Sell everything, Sell some stocks, Do nothing, Buy more stocks
	if q10.lower() == 'sell everything':
		score += 1
	elif q10.lower() == 'sell some stocks':
		score += 2
	elif q10.lower() == 'do nothing':
		score += 3.5
	elif q10.lower() == 'buy more stocks':
		score += 5
	else:
		print('not an option')

	
	#turn score into classification:
	if score <= 10:
		classification = 'Very Conservative'
	elif 10 < score <= 20:
		classification = 'Conservative'
	elif 20 < score <= 30:
		classification = 'Balanced'
	elif 30 < score <= 40:
		classification = 'Aggressive'
	elif score > 40:
		classification = 'Very Aggressive'




	return classification, score