#Create basic survey output


def risk_tolerance(args_from_ui):
	'''
	Original Function, survey questions borrowed from several sources
	including:
		- https://www.wealthfront.com/questions 
		- https://personal.vanguard.com/us/FundsInvQuestionnaire
		- http://individual.ml.com/?id=15261_45434

	Inputs:
		- args_from_ui: a dictionary with key,value pairs that correspond
					to a user's responses to questions posed in the online
					survey

	Output:
		- classification: a string indicating one of five allocations,
		based on the user's risk score
	'''

	score = 0 #initialize score to 0

	#####DEMOGRAPHIC QUESTIONS
	#q1 = How old are you?
	q1 = args_from_ui['q1']
	if int(q1) <= 55:
		if int(q1) <= 45:
			if int(q1) <= 30:
				score += 5
			elif int(q1) > 30:
				score += 3.5
		elif int(q1) > 45:
			score += 2

	#q2 = At what age do you plan to retire?
	q2 = args_from_ui['q2']
	gap = int(q2) - int(q1)
	#relevant question is how long between now and retirement

	if gap < 10:
		score -= 1
	elif gap >= 10:
		if gap >= 15:
			score +=1
			if gap >= 20:
				score +=1
				if gap >= 25:
					score +=1
					if gap >= 30:
						score += 1
						if gap >= 40:
							score += 1


	#q3 = Marital status
	q3 = args_from_ui['q3']
		
	if q3.lower() == 'single':
		score += 5
	elif q3.lower() == 'married':
		score += 2
	else: 
		pass

	#q4 = annual income
	q4 = args_from_ui['q4']
	if int(q4) >= 50000:
		score += 3
		if int(q4) >= 75000:
			score += 1.5
			if int(q4) >= 100000:
				score += 1.5
			
	#q5 = How secure are future income sources?
	q5 = args_from_ui['q5']
	if q5.lower() == "strongly agree":
		score += 7
	elif q5.lower() == "somewhat agree":
		score += 5
	elif q5.lower() == "neutral":
		score += 2
	elif q5.lower() == "somewhat disagree":
		score -= 1
	else:
		score -= 2

	####BEHAVIORAL QUESTIONS
	#q6 = what is your main goal?
	q6 = args_from_ui['q6']
	if q6.lower() == 'generating income':
		score += 2
	elif q6.lower() == 'growing wealth':
		score += 5
	else:
		pass

	#q7 = what is more important to you?
	q7 = args_from_ui['q7']
	if q7.lower() == 'maximizing gains':
		score += 7
	elif q7.lower() == 'minimizing loses':
		score -= 1
	elif q7.lower() == 'both equally':
		score += 4
	else:
		print('not an option')

	#q8 = timeline for using money
	q8 = args_from_ui['q8']
	if q8.lower() == 'a few months':
		score -= 2
	elif q8.lower() == '1-3 years':
		pass #don't change score
	elif q8.lower() == '3-5 years':
		score += 2
	elif q8.lower() == '5-10 years':
		score += 4
	elif q8.lower() == 'more than 10 years':
		score += 6
	else:
		print('not an option')

	#q9 tests risk aversion -> tradeoff between expected value and certainty
	q9 = args_from_ui['q9']
	if q9 == '$1000 @ 100% chance':
		score -= 2
	elif q9 == '$5000 @ 50% chance':
		score += 2
	elif q9 == '$100,000 at 5% chance':
		score += 6
	else:
		print('not an option')

	#tests reaction to market downturns
	q10 = args_from_ui['q10']
	if q10.lower() == 'sell everything':
		score -= 3
	elif q10.lower() == 'sell some stocks':
		score -= 1
	elif q10.lower() == 'do nothing':
		score += 2
	elif q10.lower() == 'buy more stocks':
		score += 6
	else:
		print('not an option')

	
	#turn score into classification:
	if score <= 10:
		classification = 'Very_Conservative'
	elif 10 < score <= 20:
		classification = 'Conservative'
	elif 20 < score <= 30:
		classification = 'Balanced'
	elif 30 < score <= 40:
		classification = 'Aggressive'
	elif score > 40:
		classification = 'Very_Aggressive'


	print('score = ', score)
	return classification
	