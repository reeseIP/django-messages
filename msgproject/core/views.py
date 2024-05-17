# views.py
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect
from .forms import RegisterForm


# background tasks
#from .tasks import BackgroundTasks
#t = BackgroundTasks()
#t.start()

def index(request):
	if request.user.is_authenticated:
		return render(request, 'core/index.html')
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
	response = redirect('/login/')
	return response


@login_required
def search(request, search):
	if request.method == 'POST':
		pass