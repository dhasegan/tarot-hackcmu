from django.shortcuts import render, redirect
from django.core.exceptions import ObjectDoesNotExist

from django.http import HttpResponseRedirect

# Decorator to use built-in authentication system
from django.contrib.auth.decorators import login_required

# timezone bullshit
from django.utils import timezone

# Used to create and manually log in a user
from django.contrib.auth.models import User
from django.contrib.auth import login, logout, authenticate, hashers

import datetime
import time

from app.models import *

@login_required
def discover(request):
    context = { 'page': 'discover' }
    user = QUser.objects.filter(username=request.user.username)[0]

    questionsObj = Question.objects.all()
    questions = []
    for question in questionsObj:
        midvalue = (question.maxValue - question.minValue)/2
        tr = question.timeEnd - timezone.now()
        timeremaining = str(tr.total_seconds())
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
    if (request.method != 'POST'):
        return render(request, 'types/empty.html', {})
    if not 'text' in request.POST or not request.POST['text']:
        error.append('No question')
    if not 'minval' in request.POST or not request.POST['minval']:
        error.append('No minval')
    if not 'maxval' in request.POST or not request.POST['maxval']:
        error.append('No maxval')
    if not 'time' in request.POST or not request.POST['time']:
        error.append('No time')
    if not 'date' in request.POST or not request.POST['date']:
        error.append('No date')
    text = request.POST['text']
    minval = int(request.POST['minval'])
    maxval = int(request.POST['maxval'])
    dateval = request.POST['date']
    timeval = request.POST['time']
    parsedTime = time.strptime(dateval + ' ' + timeval, "%m/%d/%y %I:%M %p")
    datetimeParsed = datetime.datetime.fromtimestamp(time.mktime(parsedTime))
    loc_dt = datetimeParsed.replace(tzinfo=timezone.get_default_timezone())
    q = Question(text=text, minValue=minval, maxValue=maxval, timeEnd=loc_dt)
    q.save()

    midvalue = (q.maxValue - q.minValue)/2
    tr = q.timeEnd - timezone.now()
    timeremaining = str(tr)
    question = {'question': q, 'timeremaining': timeremaining, 'midvalue': midvalue}

    context['question'] = question

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