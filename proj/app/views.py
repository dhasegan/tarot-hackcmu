from django.shortcuts import render, redirect
from django.core.exceptions import ObjectDoesNotExist

# Decorator to use built-in authentication system
from django.contrib.auth.decorators import login_required

# Used to create and manually log in a user
from django.contrib.auth.models import User
from django.contrib.auth import login, authenticate, hashers

from datetime import datetime

from app.models import *

# @login_required
def discover(request):
	context = {}
	return render(request, 'pages/discover.html', context)

# @login_required
def dashboard(request):
	context = {}
	return render(request, 'pages/dashboard.html', context)

# @login_required
def add_question(request):
	context = {}
	return render(request, 'types/question.html', context)

def login(request):
	context = {}
	return render(request, 'pages/login.html', context)
