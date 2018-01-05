from django.shortcuts import render, HttpResponse, redirect
from .models import *
import bcrypt
from django.contrib import messages
# Create your views here.
def index(request):
	try:
		request.session['user_id']
		return redirect('/quotes')
	except KeyError:
		return render(request, 'login_reg/index.html')
	
def register(request):
	if request.method == 'POST':
		errors = User.objects.validateUser(request.POST)
		if len(errors):
			for tag, error in errors.iteritems():
				messages.error(request, error, extra_tags=tag)
		else:
			pw_hash = bcrypt.hashpw(request.POST['password'].encode(), bcrypt.gensalt())
			# User.objects.create(name=request.POST['name'], alias=request.POST['alias'], email=request.POST['email'], password=pw_hash, dob=request.POST['dob'])
			User.objects.create(name=request.POST['name'], alias=request.POST['alias'], email=request.POST['email'], password=pw_hash, dob=request.POST['dob'])
			messages.success(request, 'Successful Register! Login, please!')
	return redirect('/')

def login(request):
	errors = User.objects.validateLogin(request.POST)
	if len(errors):
		for tag, error in errors.iteritems():
			messages.error(request, error, extra_tags=tag)
		return redirect('/')
	try:
		user = User.objects.get(email=request.POST['email'])
		print user
		password = request.POST['password']
		if bcrypt.checkpw(password.encode(), user.password.encode()):
			request.session['user_id'] = user.id
			return redirect('/quotes')
		else:
			messages.error(request, 'Password does not match!')
			return redirect('/')
	except:
		messages.error(request, "Can't find Email")
		return redirect('/')