from django.shortcuts import render, HttpResponseRedirect
from django.http import HttpResponse
from django import forms
import json
import traceback
from io import StringIO
import sys
import csv
import os
from quiz import survey
from quiz import portfolio_return
import plotly.plotly as py
import webbrowser
#Homepage when one initially visits the site!
def home(request):
	context = {}
	res = None
	if request.method == 'GET':
		form = HomePage(request.GET)

		if form.is_valid():
			if form.cleaned_data['start_quiz']:
				return HttpResponseRedirect('quiz_form')
		print (context)
	context['form'] = form
	return render(request, 'homepage.html', context)


def results(request):
	context = {}
	res = None
	investor_profile = 'This will be the explanation of your investor Profile'
	with open('etfs_text.txt') as data_file:
		etfs_text = json.load(data_file)
	with open('performance_text.txt') as data_file:
		performance_text = json.load(data_file)
	with open('worst_text.txt') as data_file:
		worst_text = json.load(data_file)	
	with open('best_text.txt') as data_file:
		best_text = json.load(data_file)

	context['investor_profile'] = investor_profile 
	context['etfs_text'] = etfs_text
	context['performance_text'] = performance_text
	context['worst_text'] = worst_text
	context['best_text'] = best_text

	return render(request, 'results.html', context)


#Classes and functions to generate the quiz form and output results
def quiz_form(request):
	context = {}
	res = None
	if request.method == 'GET':
		form = QuizForm(request.GET)
		if form.is_valid():
			args = {}
			args['q1'] = form.cleaned_data['how_old']
			args['q2'] = form.cleaned_data['when_retire']
			args['q3'] = form.cleaned_data['marital_status']
			args['q4'] = form.cleaned_data['annual_income']
			args['q5'] = form.cleaned_data['income_stability']
			args['q6'] = form.cleaned_data['main_goal']
			args['q7'] = form.cleaned_data['most_important']
			args['q8'] = form.cleaned_data['divest_in']
			args['q9'] = form.cleaned_data['game_show']
			args['q10'] = form.cleaned_data['stock_panic']
			args['q11'] = int(form.cleaned_data['principal'])
			print (args)
			try:
				profile = survey.risk_tolerance(args)
				print (profile)
			except Exception as e:
				print ('exception caught')

			return HttpResponseRedirect('results')

			# try:
			# 	annualized_return, worst_year_change, best_year_change, ETF_Names = \
			# 	portfolio_return.create_graphs(profile, args['q11'])
			# except Exception as e:
			# 	print ('exception caught')

	context['form'] = form
	return render(request, 'index.html', context)
def _is_valid(res):
	"""
	Ensures that the response from the quiz form will match the input required by survey.py

	"""
	return []



def _build_dropdown(options):
	"""
	Converts a list to a tuple with format (value, caption)

	"""
	return[(x,x) if x is not None else ('', NOPREF_STR) for x \
	in options]


#Dropdown configuration lists
MARRAIGE = _build_dropdown(['Single', 'Married', 'Other'])
STABILITY = _build_dropdown(['Strongly agree', 'Somewhat agree',\
 'Neutral','Somewhat disagree', 'Strongly disagree'])
GOALS = _build_dropdown(['Generating income', 'Growing wealth', \
	'Other'])
PRIORITIES = _build_dropdown(['Maximizing gains', 'Minimizing losses', \
	'Both equally'])
DIVESTMENT = _build_dropdown(['A few months', '1-3 years', '3-5 years',\
 '5-10 years', 'More than 10 years'])
CHANCE = _build_dropdown(['$1000 @ 100%  chance', '$5000 @ 50%  chance',\
 '$100,000 @ 5%  chance'])
PANIC = _build_dropdown(['Sell everything', 'Sell some stocks', \
 'Do nothing', 'Buy more stocks'])


class HomePage(forms.Form):
	start_quiz = forms.CharField(
		label='Please enter your name to begin the quiz',
		help_text='Our 11 question quiz will determine your investor \
		profile, and then recommend an investment portfolio that \
		matches your needs',
		required=True)
class MultipleChoice(forms.MultiValueField):
	def __init__(self, *args, **kwargs):
		fields=(forms.ChoiceField(label=None, choices=options,\
			required=True))
		super(MultipleChoice, self).__init__(
			fields=fields, *args, **kwargs)



class QuizForm(forms.Form):
	how_old = forms.CharField(
		label='1. How old are you?',
		help_text='Please enter a number between 1 and 100',
		required=True)
	when_retire = forms.CharField(
		label='2. At what age do you plan to retire?',
		help_text='Please enter a number between 1 and 100 and \
		greater than your answer to Question 1',
		required=True)
	marital_status = forms.ChoiceField(
		label='3. What is your marital status?',
		choices=MARRAIGE,
		help_text='Please select your status from the drop down \
		menu',
		required=True)
	annual_income = forms.CharField(
		label='4. What is your annual income?',
		help_text='Please enter your gross income in U.S. dollars',
		required=True)
	income_stability = forms.ChoiceField(
		label='5. My current and future income sources are very stable',
		choices=STABILITY,
		help_text='Select the statement with which you agree most',
		required=True)
	main_goal = forms.ChoiceField(
		label='6. What is your main goal in investing?',
		choices=GOALS, 
		help_text='Choose the statement that best describes your \
		investment goal',
		required=True)
	most_important = forms.ChoiceField(
		label='7. Which is more important to you?',
		choices=PRIORITIES,
		help_text='Choose an option',
		required=True)
	divest_in = forms.ChoiceField(
		label='8. When do you plan to begin using money from your \
		investments?',
		choices=DIVESTMENT,
		help_text='select a timeframe below',
		required=True)
	game_show = forms.ChoiceField(
		label='9. You are on a game show and given the choice \
		between receiving $1000, a 50%  chance to win $5,000,\
		or a 5%  chance to win $100,000. Which do you pick?',
		choices=CHANCE,
		help_text='choose one option given the the scenario above',
		required=True)
	stock_panic = forms.ChoiceField(
		label='10. The stock market drops 10%  over the course of \
		one month. What do you do?',
		choices=PANIC,
		help_text='select the option that best describes \
		your decision',
		required=True)
	principal = forms.CharField(
		label='11. What is the current amount you wish to invest?',
		help_text='Please enter an amount in USD. Do not use commas',
		required=True)




