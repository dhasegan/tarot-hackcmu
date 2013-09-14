from django.db import models

# Create your models here.
from django.contrib.auth.models import User

class QUser(User):
	score = models.FloatField()
	weight = models.FloatField()

class Question(models.Model):
	text = models.CharField(max_length=140)
	description = models.CharField(max_length=1000)
	timeStart = models.DateField(auto_now=True)
	timeEnd = models.DateField()
	minValue = models.FloatField()
	maxValue = models.FloatField()
	upvote = models.IntegerField()
	downvote = models.IntegerField()

class Answer(models.Model):
	user = models.ForeignKey(BidUser);
	question = models.ForeignKey(Question)
	value = models.FloatField()
	timeSubmit = models.DateField(auto_now=True)