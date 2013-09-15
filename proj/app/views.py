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
import updatescores

@login_required
def home(request):
    return redirect('/discover/')

@login_required
def discover(request):
    context = { 'page': 'discover' }
    user = QUser.objects.filter(username=request.user.username)[0]

    questionsObj = Question.objects.all()
    questions = []
    for question in questionsObj:
        midvalue = (question.maxValue - question.minValue)/2
        tr = question.timeEnd - timezone.now()
        if (tr.total_seconds() > 0) and len(Answer.objects.filter(user=user, question=question))==0:
            timeremaining = str(tr.total_seconds())
            questions.append( {'question': question, 'timeremaining': timeremaining, 'midvalue': midvalue} )

    tn = timezone.now()
    questions.sort(key=lambda x: (x['question'].timeEnd-tn).total_seconds())

    context['useranswered'] = len(Answer.objects.filter(user=user))
    context['userscore'] = user.score
    context['questions'] = questions
    return render(request, 'pages/discover.html', context)

@login_required
def dashboard(request):
    context = { 'page': 'dashboard' }
    user = QUser.objects.filter(username=request.user.username)[0]

    update_scores()

    questionsObj = Question.objects.all()
    questions = []
    for question in questionsObj:
        tr = question.timeEnd - timezone.now()
        answers = Answer.objects.filter(user=user, question=question)
        if len(answers) > 0:
            midvalue = answers[0].value
            if (tr.total_seconds() > 0):
                timeremaining = str(tr.total_seconds())
            else:
                timeremaining = str(0)
            questions.append( {'question': question, 'timeremaining': timeremaining, 'midvalue': midvalue} )

    tn = timezone.now()
    questions.sort(key=lambda x: (x['question'].timeEnd-tn).total_seconds())
            
    context['questions'] = questions
    context['userscore'] = user.score
    context['useranswered'] = len(Answer.objects.filter(user=user))
    return render(request, 'pages/dashboard.html', context)

@login_required
def add_question(request):
    context = { 'page': 'discover' }
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

    midvalue = (q.maxValue - q.minValue)/2 + q.minValue
    tr = q.timeEnd - timezone.now()
    timeremaining = str(tr.total_seconds())
    question = {'question': q, 'timeremaining': timeremaining, 'midvalue': midvalue}

    context['question'] = question

    return render(request, 'types/question.html', context)

@login_required
def add_answer(request):
    context = {}
    if (request.method != 'POST'):
        return render(request, 'types/empty.html', {})
    if not 'id' in request.POST or not request.POST['id']:
        error.append('No id')
    if not 'ans' in request.POST or not request.POST['ans']:
        error.append('No ans')
    qid = int(request.POST['id'])
    ans = float(request.POST['ans'])

    question = Question.objects.filter(id=qid)[0]
    user = QUser.objects.filter(username=request.user.username)[0]

    if len(Answer.objects.filter(user=user, question=question)) > 0:
        return render(request, 'types/empty.html', context);

    answer = Answer(user=user, question=question, value=ans)
    answer.save()

    return render(request, 'types/empty.html', context)

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
                user = authenticate(username=request.POST['userName'], \
                    password=request.POST['userPassword'])
                if (user != None):
                    login(request, user)
                    return redirect("/discover")
                else:
                    return redirect("/login")
        else:
            if (len(request.POST['userPassword']) > 0):
                new_user = QUser.objects.create_user(username=request.POST['userName'], \
                    password=request.POST['userPassword'],score=0.0,weight=0.5)
                new_user.save()
                new_user = authenticate(username=request.POST['userName'], \
                    password=request.POST['userPassword'])
                login(request, new_user)
                return redirect("/discover")

    if errors:
        return render(request, 'pages/login.html', context)

    return render(request, 'pages/login.html', context)

def update_scores():
    questions = Question.objects.filter(trueval__isnull=True)
    for i in range(0,len(questions)):
        if(questions[i].trueval!=None and questions[i].timeEnd < timezone.now() ):
            u_list = {}
            v_list = []
            # q_list.append(questions[i-1])
            temp_1 = Answer.objects.filter(question = questions[i])
            if (len(temp_1) == 0):
                continue
            for j in range(len(temp_1)):
                v_list.append((temp_1[j].user.username,temp_1[j].value))  # votes information
                user = QUser.objects.all().filter(username = temp_1[j].user.username)[0]
                u_list[user.username] = [user.weight, user.score] # user weight and score information

            (results, q_trueval) = updatescores.parseVotes(v_list,u_list)                 # the updates for user sweights and scores the trueval of the question
            q_score_update = questions[i]
            q_score_update.trueval = q_trueval
            q_score_update.save()
            for k in range(len(results)):
                username = v_list[k][0]
                u_update = QUser.objects.all().filter(username=username)[0]
                u_update.weight =  results[username][0]
                u_update.score = results[username][1]
                u_update.save()






