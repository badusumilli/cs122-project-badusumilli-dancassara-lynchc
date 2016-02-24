from django.shortcuts import HttpResponse

def index(request):
	return HttpResponse ("Polls index")

def detail(request, quiz_id):
	return HttpResponse("Quiz %s." % quiz_id)

def results(request, quiz_id):
	response = "Results of Question %s." 
	return HttpResponse(response %quiz_id)

def vote(request, quiz_id):
	return HttpResponse("Please answer Question %s." % quiz_id)

def quiz(request, quiz_id):
	return HttpResponse("Quiz %s." % quiz_id)



# Create your views here.
