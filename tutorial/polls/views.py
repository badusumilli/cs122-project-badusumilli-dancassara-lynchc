from django.shortcuts import HttpResponse
from django import forms





def index(request):
	return HttpResponse ("Polls index")

def detail(request, quiz_id):
	return HttpResponse("Quiz %s." % quiz_id)

def results(request, quiz_id):
	response = "Results of Quiz %s." 
	return HttpResponse(response %quiz_id)

def vote(request, quiz_id):
	return HttpResponse("Complete the quiz below to determine your investment\
     profile %s." % quiz_id)

def quiz(request, quiz_id):
	return HttpResponse("Quiz %s." % quiz_id)

class Quizform(forms.Form):
    q1 = forms.CharField(
        label= "How old are you?"
        help_text = 'e.g. 22'
        required=True)
    q2 = 

# Create your views here.
