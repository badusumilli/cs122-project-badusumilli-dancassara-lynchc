#Create basic survey output


def risk_tolerance(args_from_ui):

	score = 0
	#####DEMOGRAPHIC QUESTIONS


	score = 0
	#####DEMOGRAPHIC QUESTIONS
	q1 = args_from_ui['q1']
	if int(q1) <= 55:
		if int(q1) <= 45:
			if int(q1) <= 30:
				score += 5
			elif int(q1) > 30:
				score += 3.5
		elif int(q1) > 45:
			score += 2

	q2 = args_from_ui['q2']
	gap = int(q2) - int(q1)

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


	# print()
	# print('Options: Single, Married, Other')
	q3 = args_from_ui['q3']
		#Options: Single, Married, Divorced
		
	if q3.lower() == 'single':
		score += 5
	elif q3.lower() == 'married':
		score += 2
	else: 
		pass

	print()
	q4 = args_from_ui['q4']
	if int(q4) >= 50000:
		score += 3
		if int(q4) >= 75000:
			score += 1.5
			if int(q4) >= 100000:
				score += 1.5
			
	# print()
	# print('Options: Strongly agree, somewhat agree, neutral, somewhat disagree, strongly disagree')
	q5 = args_from_ui['q5']
		#Options: Strongly agree, somewhat agree, neutral, somewhat disagree, strongly disagree	
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
	
	q6 = args_from_ui['q6']
	if q6.lower() == 'generating income':
		score += 2
	elif q6.lower() == 'growing wealth':
		score += 5
	else:
		pass

	q7 = args_from_ui['q7']
		#Options: maximizing, minimizing, both equally
	if q7.lower() == 'maximizing gains':
		score += 7
	elif q7.lower() == 'minimizing loses':
		score -= 1
	elif q7.lower() == 'both equally':
		score += 4
	else:
		print('not an option')


	q8 = args_from_ui['q8']
		#Options: A few months, 1-3 years, 3-5 Years, 5-10 Years, More than 10 years 
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

	# print()
	# print('Options: 1000, 5000, 100000')
	q9 = args_from_ui['q9']
		#Options: 1000, 5000, 100000
	if q9 == '$1000 @ 100% chance':
		score -= 2
	elif q9 == '$5000 @ 50% chance':
		score += 2
	elif q9 == '$100,000 at 5% chance':
		score += 6
	else:
		print('not an option')

	# print()
	# print('Options: Sell everything, Sell some stocks, Do nothing, Buy more stocks')
	q10 = args_from_ui['q10']
		#Options: Sell everything, Sell some stocks, Do nothing, Buy more stocks
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
	