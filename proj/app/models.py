from django.db import models

# Create your models here.
from django.contrib.auth.models import User

class QUser(User):
	score = models.FloatField({ 'default': 0.0 })
	weight = models.FloatField({ 'default': 0.50 })

class Question(models.Model):
	text = models.CharField(max_length=140)
	description = models.CharField(max_length=1000)
	timeStart = models.DateTimeField(auto_now=True)
	timeEnd = models.DateTimeField()
	minValue = models.FloatField()
	maxValue = models.FloatField()
	upvote = models.IntegerField(default= 0, null=True, blank=True)
	downvote = models.IntegerField(default= 0, null=True, blank=True)

class Answer(models.Model):
	user = models.ForeignKey(QUser);
	question = models.ForeignKey(Question)
	value = models.FloatField()
	timeSubmit = models.DateTimeField(auto_now=True)