from django.shortcuts import render, HttpResponse, redirect
from models import * #grabbing classes from models.py
from django.contrib import messages #importing messaging function
from datetime import datetime #importing for datetime to function
import random #importing for random interge values in range defined below


#Main landing for logon and registration page:
def index(request):
    return render(request, "main_app/index.html")

#User registration section:
def register(request):
	results = User.objects.regVal(request.POST)
	if results['status'] == False:
		for error in results['errors']:
			messages.error(request, error)
		return redirect('/')
	user = User.objects.creator(request.POST)
	messages.success(request, 'User has been created. Please log in to continue')
	return redirect('/')

#User login section:
def login(request):
	results = User.objects.logVal(request.POST)
	if results['status'] == False:
		for error in results['errors']:
			messages.error(request, error)
		return redirect('/')
	request.session['id'] = results['user'].id
	request.session['name'] = results['user'].name
	return redirect('/home') #redirect to home method and render html page noted in 'home' --> home_screen

def home(request): ##Creates table for top 5 players by gold, decending
    if sessCheck(request) == False:
        return redirect('/')

    context = {
        'user': User.objects.all().order_by('-gold')[:05] # Statement to list top five players via range (0-5)
    }
    return render(request, 'main_app/home_screen.html', context)

#Just use it...
def sessCheck(request):
    print request.session['name']
    try:
        return request.session['name']
    except:
        return False

#User logout:
def logout(request):
    request.session.flush()
    return redirect('/')

#Need to use next two (all_users and player) together, along with adding to urls.py
def all_users(request):
    context = {
    "user": User.objects.all().order_by('-gold')
    }
    return render(request, "main_app/all_users.html", context)

def player(request, player_id):
    context = {
        "player": User.objects.get(id=player_id)
    }
    return render(request, "main_app/player.html", context)

#Adding component to play game
def play_game(request):
    context = {
        "user": User.objects.get(id=request.session['id']) #build user key by id
    }
    try:
        request.session['gold']
    except KeyError:
        request.session['gold'] = 0
        ##If gold is less than 0, kill session and delete user
    if request.session['gold'] < 0:
        user = User.objects.get(id=request.session['id'])
        user.delete()
        for key in request.session.keys():
            del request.session[key]
        return redirect('/')
    return render(request, "main_app/play_game.html", context)

#Game logic:
def process(request):
    # print "==============="
    # print request.POST.keys()
    # p = Logs.objects.all() #Testing logging of objects
    # print p
    # print "==============="
    if request.POST['building'] == 'cave':
        request.session['gold'] += random.randrange(1,10)
        new = Logs.objects.create(content='You got gold from the cave', user=User.objects.get(id=request.session['id']))
    if request.POST['building'] == 'house':
        request.session['gold'] += random.randrange(-5, 10)
        new = Logs.objects.create(content='You lost gold from the house', user=User.objects.get(id=request.session['id']))
    if request.POST['building'] == 'farm':
        request.session['gold'] += random.randrange(0,20)
        new = Logs.objects.create(content='You got gold from the farm', user=User.objects.get(id=request.session['id']))
        new.save()
    g = User.objects.get(id=request.session['id'])
    g.gold = request.session['gold']
    g.save()
    return redirect('/play_game')

#Clear Session Keys
def clear(request):
    for key in request.session.keys():
        del request.session[key]
    return redirect('/')
