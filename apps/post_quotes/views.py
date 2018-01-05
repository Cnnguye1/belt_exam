from django.shortcuts import render, redirect, HttpResponse
from ..login_reg.models import *
from .models import *
from django.contrib import messages

# Create your views here.

def quotes(request):
	context = {
		'user': User.objects.get(id= request.session['user_id']),
		'quotes': Quote.objects.all().exclude(user_favorites=User.objects.get(id=request.session['user_id'])).order_by('-created_at'),
		'user_favorites_quotes': Quote.objects.filter(user_favorites=User.objects.get(id=request.session['user_id']))
	}
	return render(request, 'post_quotes/quotes.html', context)

def user(request, user_id):
	context = {
	'user': User.objects.get(id=user_id),
	'user_quotes': Quote.objects.filter(post_by=User.objects.get(id=user_id))
	}
	return render(request, 'post_quotes/post_by.html', context)

def delete(request, quote_id):
	quote = Quote.objects.get(id=quote_id, post_by=User.objects.get(id=request.session['user_id']))
	quote.delete()
	return redirect('/quotes')

def add(request, quote_id):
	user = User.objects.get(id=request.session['user_id'])
	quote = Quote.objects.get(id=quote_id)
	quote.user_favorites.add(user)
	return redirect('/quotes')

def remove(request, quote_id):
	user = User.objects.get(id=request.session['user_id'])
	quote = Quote.objects.get(id=quote_id, user_favorites= user)
	quote.user_favorites.remove(user)
	return redirect('/quotes')

def create(request):
	if request.method == 'GET':
		return redirect('/quotes')
	else:
		errors = Quote.objects.validateQuote(request.POST)
		if len(errors):
			for tag, error in errors.iteritems():
				messages.error(request, error, extra_tags=tag)
			return redirect('/')
		else:
			Quote.objects.create(name=request.POST['name'], message=request.POST['message'], post_by=User.objects.get(id=request.session['user_id']))
			return redirect('/')

def log_out(request):
	for key in request.session.keys():
		del request.session[key]
	return redirect('/')

