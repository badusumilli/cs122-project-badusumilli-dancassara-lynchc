from __future__ import unicode_literals
from django.contrib import admin
from .models import Quiz, Question, Choice, Response
from django.db import models
from django.utils import timezone
import datetime

admin.site.register(Quiz)


# Register your models here.
