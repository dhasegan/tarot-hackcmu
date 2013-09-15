from django.shortcuts import render, redirect
from django.core.exceptions import ObjectDoesNotExist

from django.http import HttpResponseRedirect

# Decorator to use built-in authentication system
from django.contrib.auth.decorators import login_required

# Used to create and manually log in a user
from django.contrib.auth.models import User
from django.contrib.auth import login, logout, authenticate, hashers

import datetime

from app.models import *

@login_required
def discover(request):
    context = { 'page': 'discover' }
    user = QUser.objects.filter(username=request.user.username)[0]

    questionsObj = Question.objects.all()
    questions = []
    for question in questionsObj:
        midvalue = (question.maxValue - question.minValue)/2
        tr = question.timeEnd - datetime.datetime.now()
        timeremaining = datetime.datetime.strptime(tr, '%H:%M:%S')
        questions.append( {'question': question, 'timeremaining': timeremaining, 'midvalue': midvalue} )
    context['questions'] = questions
    return render(request, 'pages/discover.html', context)

@login_required
def dashboard(request):
    context = {}
    return render(request, 'pages/dashboard.html', context)

@login_required
def add_question(request):
    context = {}
    return render(request, 'types/question.html', context)

def signout(request):
    logout(request)
    return redirect('/login/')

def signup(request):
    context = { 'page': "login" }
    if request.user and request.user.is_authenticated():
        return redirect('/discover/')

    if (request.method == 'GET'):
        return render(request, 'pages/login.html', {})

    errors = []
    context['errors'] = errors

    if not 'userName' in request.POST:
        errors.append('Username is required.')
    if not 'userPassword' in request.POST:
        errors.append('Password is required.')
    else:
        if (len(QUser.objects.filter(username = request.POST['userName'])) > 0):
            user = QUser.objects.filter(username = request.POST['userName'])[0]
            if (user.check_password(request.POST['userPassword'])):
                return redirect("/discover")
        else:
            if (len(request.POST['userPassword']) > 0):
                new_user = QUser.objects.create_user(username=request.POST['userName'], \
                    password=request.POST['userPassword'],score=0,weight=0)
                new_user.save()
                new_user = authenticate(username=request.POST['userName'], \
                    password=request.POST['userPassword'])
                login(request, new_user)
                return redirect("/discover")

    if errors:
        print errors
        return render(request, 'pages/login.html', context)

    return render(request, 'pages/login.html', context)