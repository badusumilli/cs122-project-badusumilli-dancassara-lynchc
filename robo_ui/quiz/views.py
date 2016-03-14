from django.shortcuts import render, HttpResponseRedirect
from django.http import HttpResponse
from django import forms
import json
import traceback
from io import StringIO
import sys
import csv
import os
from quiz import survey, portfolio_return
import plotly.plotly as py
import webbrowser
import re
#Homepage when one initially visits the site!
def home(request):
	"""
	Generates the homepage for the app, using homepage.html

	"""
	context = {}
	res = None
	if request.method == 'GET':
		form = HomePage(request.GET)

		if form.is_valid():
			if form.cleaned_data['start_quiz']:
				return HttpResponseRedirect('quiz_form')
		print (context)
	#create dictionary for text displayed on homepage 
	context['explanation_text'] = 'Our 11 question quiz will determine \
	your investor profile, and then recommend an investment portfolio that \
		matches your needs'
	context['error_message'] = 'Each field is Required!'
	context['form'] = form
	return render(request, 'homepage.html', context)

def helper():
	"""
	Called by results(), function reads in stored json text and \
	generates the context dict to go to results.html

	"""
	context = {}
	res = None

	#read saved information from portfolio_return.py
	with open('quiz/temp_json_files/profile.txt') as data_file:
		profile = json.load(data_file)
	with open('quiz/temp_json_files/allocation_text.txt') as data_file:
		allocation_text = json.load(data_file)
	with open('quiz/temp_json_files/etfs_text.txt') as data_file:
		etfs_text = json.load(data_file)
		etfs_list = etfs_text.split(',')

	with open('quiz/temp_json_files/performance_text.txt') as data_file:
		performance_text = json.load(data_file)
	with open('quiz/temp_json_files/worst_text.txt') as data_file:
		worst_text = json.load(data_file)	
	with open('quiz/temp_json_files/best_text.txt') as data_file:
		best_text = json.load(data_file)

	#adds text to the context dict for results.html
	context['profile'] = profile 
	context['allocation_text'] = allocation_text
	context['etfs_list'] = etfs_list
	context['performance_text'] = performance_text
	context['worst_text'] = worst_text
	context['best_text'] = best_text
	context['vanguard_link'] = 'https://investor.vanguard.com/etf/'

	return context

def results(request):
	"""
	Generates the page to display the information and graphs for\
	a given investment portfolio. calls information from saved json files \
	and fixed urls using helper(), and provides the option to go to more or \
	less agressive profiles. Generates the page from results.html

	"""
	
	context = helper()
	profile = context['profile']
	allocations = ['Very_Conservative', 'Conservative', 'Balanced', 'Aggressive', 'Very_Aggressive']
	x = allocations.index(profile)
	if request.method == 'GET':
		if 'home' in request.GET:
				return HttpResponseRedirect('/quiz')
	#loads the results page for the next most agressive profile
	if 'more' in request.GET:
		if x != len(allocations)-1:
			x = x + 1
			print(x)
			profile = allocations[x]
			shit = portfolio_return.create_graphs_and_text(profile, 10000)
			context = helper()
			return render(request, 'results.html', context)
		else:
			return HttpResponse("Can't get more Agressive!")
	#loads the results page for the next least agressive profile
	if 'less' in request.GET:
		if x != 0:
			x = x - 1
			print (x)
			profile = allocations[x]
			print (profile)
			shit = portfolio_return.create_graphs_and_text(profile, 10000)
			context = helper()
			return render(request, 'results.html', context)
		else:
			return HttpResponse("Can't get less Agressive!")
	

	return render(request, 'results.html', context)


#Classes and functions to generate the quiz form and output results
def quiz_form(request):
	"""
	View function for the quiz form page. Generates an 11 question quiz \
	with charfield and choicefield values, then passes the responses to \
	survey.py for scoring, the profile returned by the survey function \
	is passed to portfolio_return.py for graph and text generation. 

	"""
	context = {}
	res = None
	#generate web form
	if request.method == 'GET':
		#links back to homepage to start over
		if 'home' in request.GET:
				return HttpResponseRedirect('/quiz')
		#check to see if the form has been filled out
		#clean values and create args dict
		form = QuizForm(request.GET)
		if form.is_valid():

			args = {}
			args['q1'] = form.cleaned_data['how_old']
			args['q2'] = form.cleaned_data['when_retire']
			args['q3'] = form.cleaned_data['marital_status']

			args['q4'] = form.cleaned_data['annual_income'].replace(',', '')
			args['q4'] = re.findall('[0-9]+', args['q4'])
			args['q4'] = args['q4'][0]

			args['q5'] = form.cleaned_data['income_stability']
			args['q6'] = form.cleaned_data['main_goal']
			args['q7'] = form.cleaned_data['most_important']
			args['q8'] = form.cleaned_data['divest_in']
			args['q9'] = form.cleaned_data['game_show']
			args['q10'] = form.cleaned_data['stock_panic']

			args['q11'] = form.cleaned_data['principal'].replace(',', '')
			args['q11'] = re.findall('[0-9]+', args['q11'])
			args['q11'] = int(args['q11'][0])

			#pass args dict to survey.py for scoring 
			try:
				profile = survey.risk_tolerance(args)
			except Exception as e:

				print (e)
			#pass profile from survey.py to portfolio_return.py for \
			#text and graph generation
			try:
				portfolio_return.create_graphs_and_text(profile, args['q11'])
			except Exception as e:
				print (e)
			#load results page
			return HttpResponseRedirect('results')
	#if the form was not filled out/not properly filled out, reject the \
	#submission and re-load the page
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


#Dropdown configuration lists, correspond to keys in survey.py
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
	"""
	Class to generate the homepage input form, links to the home function.
	"""
	start_quiz = forms.CharField(
		label='Please enter your name to begin the quiz',
		help_text=None,
		required=True)

class QuizForm(forms.Form):
	"""
	Class to generate the quiz form at /quiz/quiz_form, links to the \
	quiz_form function

	"""
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




