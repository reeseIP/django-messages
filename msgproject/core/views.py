# views.py
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.core.signing import Signer
from django.db import IntegrityError
from django.http import HttpResponse,JsonResponse
from django.shortcuts import render, redirect
from .forms import RegisterForm
from .models import ExternalSystems, ExternalUsers

import requests


# background tasks
from .tasks import BackgroundTasks
t = BackgroundTasks()
t.start()

def index(request):
	if request.user.is_authenticated:
		try:
			theme = request.COOKIES['theme']
		except KeyError:
			theme = 'light'
		return render(request, 'core/index.html', {'theme': theme})
	else:
		return redirect('/login')


# Create your views here.
def register_user(request):
	if request.method == 'GET':
		form = RegisterForm()
		return render(request, 'core/register.html', {'form': form})
	elif request.method == 'POST':
		form = RegisterForm(request.POST)
		if form.is_valid():
		    form.save()
		    username = request.POST["username"]
		    password = request.POST["password1"]
		    user = authenticate(request, username=username, password=password)
		    if user is not None:
		    	login(request, user)
		    	return redirect('/')
		else:
			messages.error(request,form.errors)
			return render(request, 'core/register.html', {'form': form})


def login_user(request):
	if request.method == 'GET':
		if request.user.is_authenticated:
			return redirect('/')
		return render(request, 'core/login.html')
	elif request.method == 'POST':
		username = request.POST["username"]
		password = request.POST["password"]
		user = authenticate(request, username=username, password=password)
		if user is not None:
			login(request, user)
			return redirect('/')
		else:
			messages.error(request, 'Invalid Credentials')
			return render(request, 'core/login.html')


@login_required
def logout_user(request):
	#tar_sys_users = ExternalUsers.objects.filter(created_by=request.user).delete()
	logout(request)
	return JsonResponse({'status_code': 200})


@login_required
def set_target_user(request, service, system, username):
	''' set a user for an external system '''
	if request.method == 'POST':
		ext_user = username
		ext_sys = ExternalSystems.objects.filter(system=system, service=service).first()

		user = ext_sys.users.filter(created_by=request.user,username=ext_user).first()
		active_user = ext_sys.users.filter(created_by=request.user,active=True).first()
		if user:
			if active_user:
				active_user.active = False
				active_user.save()
			user.active = True
			user.save()
			return JsonResponse({'status_code': 200})
		else:
			#tar_sys = ExternalSystems.objects.filter(system=system, service=g_service).first()
			# validate user credentials in external system
			response = requests.get(ext_sys.url,
										auth=(username,request.POST["password"]))
			if response:
				if response.status_code == 200:
					signer = Signer()
					user = ExternalUsers()
					user.username = username 
					user.password = signer.sign_object({'password':request.POST["password"]})
					#user.csrf_token = request.POST["csrfmiddlewaretoken"]
					user.sessionid = request.POST["sessionid"]
					user.system_id = ext_sys.id
					user.created_by = request.user
					user.active = True
					try:
						user.save()
						if active_user:
							active_user.active = False
							active_user.save()
						messages.success(request, 'Temporary User {} Created'.format(user.username))
						return JsonResponse({'status_code': 200})
					except IntegrityError:
						pass
				
			messages.error(request, 'Invalid User')
			return JsonResponse({'status_code': 500})


@login_required
def delete_target_user(request, service, system, username):
	''' delete an external user '''
	if request.method == 'POST':
		ext_sys = ExternalSystems.objects.filter(system=system, service=service).first()
		user = ext_sys.users.filter(username=username, created_by=request.user)
		if user.delete()[1]:
			status_code = 200
		else:
			status_code = 500

		return JsonResponse({'status_code': status_code})


@login_required
def search(request, search):
	if request.method == 'POST':
		pass