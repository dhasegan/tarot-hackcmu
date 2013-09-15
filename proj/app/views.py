from django.shortcuts import render, redirect
from django.core.exceptions import ObjectDoesNotExist

from django.http import HttpResponseRedirect

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
    context = { 'page': "login" }       

    errors = []
    context['errors'] = errors
        
    # username
    if not 'userName' in request.POST:  
        # print "no username in request"
        errors.append('Username is required.')        
    if not 'userPassword' in request.POST:          
        # print "no password in request"
        errors.append('Password is required.')        
    else:       
        if (len(QUser.objects.filter(username = request.POST['userName'])) > 0):            
            user = QUser.objects.filter(username = request.POST['userName'])[0]
            if (user.check_password(request.POST['userPassword'])):
            #print "username found in db"
                return HttpResponseRedirect("pages/discover.html")            
            # errors.append('Username is already taken.')                    	
        else:
            if (len(request.POST['userPassword']) > 0):
                new_user = QUser.objects.create_user(username=request.POST['userName'], \
                    password=request.POST['userPassword'],score=0,weight=0)        	            
                # print "new username is created"
                new_user.save()
                # print "username saved"
                # return redirect('pages/discover.html')
                return HttpResponseRedirect("pages/discover.html")               

    if errors:
        # print "some errors"
        return render(request, 'pages/login.html', context)        
    
    return render(request, 'pages/login.html', context)