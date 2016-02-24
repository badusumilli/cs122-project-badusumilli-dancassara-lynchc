from __future__ import unicode_literals

from django.contrib.auth.models import User
from django.db import models
from django.utils import timezone
#from django import forms
import datetime

class Quiz(models.Model):
	title = models.CharField(max_length=60, blank=False,)
	pub_date = models.DateTimeField('date published')

	#show_feedback = models.BooleanField(blank=False, default=True, help_text='')

	class Meta: 
		verbose_name = "Quiz"
		verbose_name_plural = "Quizzes"


	def __unicode__(self):
		return self.title


class Question(models.Model):
	question_text = models.CharField(max_length=200)
	pub_date = models.DateTimeField('date published')

	def __str__(self):
		return self.question_text

	# def __repr__(self):
	# 	return 'question_text, pub_date({}, {})'.format(self.question_text, self.pub_date)

	def was_published_recently(self):
		return self.pub_date   >= timezone.now() - datetime.timedelta(days=1)



class Choice(models.Model):
	question = models.ForeignKey(Question, on_delete=models.CASCADE)
	choice_text = models.CharField(max_length=200)
	choice_index = models.IntegerField(default=0)
	multi1 = models.CharField(max_length=200, default=None)
	multi2 = models.CharField(max_length=200, default=None)
	multi3 = models.CharField(max_length=200, default=None)
	multi4 = models.CharField(max_length=200, default=None)
	multi5 = models.CharField(max_length=200, default=None)

	def __str__(self):
		return self.choice_text

	def set_choice(self, votes):
		choice_list = ['index burner', models.multi1, models.multi2, models.multi3,\
		models.multi4, models.multi5]
		if models.choice_index != 0:
			pass


class Response(models.Model):
	user = models.ForeignKey(User)
	question = models.ForeignKey(Question)

	class Meta: 
		abstract = True

class freeResponse(Response):
	free_response = models.TextField(max_length=200, blank=True)

class multipleChoiceResponse(Response):
	answer = models.ForeignKey(Choice)




#add forms class for the questions page views/details or soemthign like that 
# Create your models here.
