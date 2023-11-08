from django.contrib import messages
from django.shortcuts import get_object_or_404, render, redirect
from django.http import HttpResponse
from django.forms import formset_factory
from django.views.decorators.csrf import csrf_exempt
from .models import OrderJobData, OrderTaskData, PutawayJobData, PutawayTaskData
from .forms import TaskDataForm

from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.conf import settings

import json
import requests
import io
import base64

# Create your views here.

### helper methods
def send_request(request,job_data,job_type,event_type,event_info=None,tasks=None):
	if job_type == 'OrderJob':
		job_message = {"OrderJobResult": {"EventType":event_type,
											"EventInfo":None,
											"JobId":job_data["JobId"],
											"JobStatus":"Completed",
											"JobDate":"Date",
											"JobStation":None,
											"RequestId":job_data["RequestId"],
											"ToteId":job_data["ToteId"],
											"JobRobot":None,
											"JobMethod":None,
											"JobTasks": [tasks]
											}}
	elif job_type == 'PutawayJob':
		job_message = {'PutawayJobResult': {"EventType":event_type,
											"EventInfo":None,
											"LicensePlate":job_data['LicensePlate'],
											"RequestId":job_data['RequestId'],
											"JobId":job_data['JobId'],
											"JobDate":'Date',
											"JobStatus":'Completed',
											"JobStation":None,
											"JobRobot":None,
											"JobTasks": [tasks]
											}}	

	client = requests.session()
	# URL = settings.PROD_POST_URL
	# client.auth = settings.PROD_POST_AUTH
	#response = requests.post(URL,
	#						json=json.dumps(job_message))

	# local testing
	URL = settings.TEST_POST_URL
	client.auth = settings.TEST_POST_AUTH
	response = client.post(URL,
							json=json.dumps(job_message))

	if response.status_code == '200':
		messages.success(request, response.text)
	elif response.status_code != '200':
		messages.error(request, response.text)

	return response.status_code

def get_job(JobId):
	try:
		job = OrderJobData.objects.filter(JobId=JobId)[0]
		job_type = 'OrderJob'
	except IndexError:
		job = get_object_or_404(PutawayJobData, JobId=JobId)
		job_type = 'PutawayJob'
	
	job_data = job.get_data()
	return job_data, job_type



### view methods
def login_user(request):
	if request.method == 'GET':
		return render(request, 'messagelocus/login.html')
	elif request.method == 'POST':
	    username = request.POST["username"]
	    password = request.POST["password"]
	    user = authenticate(request, username=username, password=password)
	    if user is not None:
	    	login(request, user)
	    	return redirect('/messagelocus/')
	    else:
	    	messages.error(request, 'Invalid Credentials')
	    	return render(request, 'messagelocus/login.html')

@login_required
def logout_user(request):
	logout(request)
	return redirect('/messagelocus/login/')

@login_required
def index(request):
	''' landing page - list of jobs'''
	orderjob_list = OrderJobData.objects.order_by('-JobId')[:]
	putawayjob_list = PutawayJobData.objects.order_by('-JobId')[:]
	context = {
		'orderjob_list': orderjob_list,
		'putawayjob_list': putawayjob_list,
	}
	return render(request, 'messagelocus/index.html', context)

@csrf_exempt
def inbound(request):
	''' inbound messages '''
	if request.method == 'POST':
		auth_header = request.META['HTTP_AUTHORIZATION']
		encoded_credentials = auth_header.split(' ')[1]  # Removes "Basic " to isolate credentials
		decoded_credentials = base64.b64decode(encoded_credentials).decode("utf-8").split(':')
		username = decoded_credentials[0]
		password = decoded_credentials[1]
		user = authenticate(request, username=username, password=password)
		if user is not None:
			json_data = json.loads(json.load(io.BytesIO(request.body)))
			for k1, v1 in json_data.items():
				# outermost structure (Message Type)
				if k1 == 'OrderJob':
					job_model = OrderJobData
					task_model = OrderTaskData
				elif k1 == 'PutawayJob':
					job_model = PutawayJobData
					task_model = PutawayTaskData
				else:
					return HttpResponse('Error - Incorrect Message Type')
				query = job_model.objects.filter(JobId=v1['JobId'])
				if query:
					# job already exists
					job_data, job_type = get_job(JobId=query[0].JobId)
					return HttpResponse(send_request(request,job_data,job_type,"REJECT","Rejected - Job Already Exists"))
				else:
					# new job
					fields = job_model._meta.get_fields()
					new_job = job_model()
					for field in fields:
						try:
							value = v1[field.name]
						except KeyError: # field was not supplied
							value = None
						setattr(new_job,field.name,value)
					
					new_job.save()

					# new tasks
					job_tasks = v1['JobTasks']
					# task_type will be either OrderJobTask or PutawayJobTask for key
					# and a list of tasks for value
					for task_type, tasks in job_tasks.items():
						fields = task_model._meta.get_fields()
						for task in tasks:
							new_task = task_model()
							for field in fields:
								if field.name == 'JobId':
									value = new_job
									setattr(new_task,field.name,value)
								else:
									try:
										value = task[field.name]
										if value == 'false':
											value = False 
										elif value == 'true':
											value = True
									except KeyError: # field was not supplied
										value = None
									setattr(new_task,field.name,value)

							new_task.save()
		else:
			return HttpResponse('Invalid Credentials')


		return HttpResponse('Ive Been hit')
	else:
		return HttpResponse('Inbound Request - GET')

@login_required
def jobview(request, JobId):
	''' overview for job details'''
	TaskDataFormSet = formset_factory(TaskDataForm, extra=0)
	
	job_data, job_type = get_job(JobId=JobId)

	tasks = OrderTaskData.objects.filter(JobId_id=job_data['id']).order_by('JobTaskId')[:]
	if not tasks.exists():
		tasks = PutawayTaskData.objects.filter(JobId_id=job_data['id']).order_by('JobTaskId')[:]

	del job_data['id'] # dont want to pass this to the html template
	task_data = []
	task_header = []
	for task in tasks:
		task_data.append(task.get_data())
	for item in task_data:
		for key, value in item.items():
			task_header.append(key)
		break

	formset = TaskDataFormSet(initial=task_data)
	for form in formset:
		for field in form:
			task_header.append(field.label)

	task_header = list(dict.fromkeys(task_header))

	return render(request, "messagelocus/jobview.html", {'JobId': JobId,
														 'job_data': job_data,
														 'task_data': task_data,
														 'task_header': task_header,
														 'formset': formset,
														 })

@login_required
def sendaccept(request, JobId):
	''' send an ACCEPT message for job '''
	job_data, job_type = get_job(JobId=JobId)
	send_request(request,job_data,job_type,"ACCEPT")
	return redirect('/messagelocus/{}'.format(JobId))

@login_required
def sendreject(request, JobId):
	''' send a REJECT message for job '''
	job_data, job_type = get_job(JobId=JobId)
	send_request(request,job_data,job_type,"REJECT","Rejected - Manually Posted")
	return redirect('/messagelocus/{}'.format(JobId))

@login_required
def sendtoteinduct(request, JobId):
	''' send a TOTEINDUCT message for job '''
	job_data, job_type = get_job(JobId=JobId)
	send_request(request,job_data,job_type,"TOTEINDUCT")
	return redirect('/messagelocus/{}'.format(JobId))

@login_required
def sendpickcomplete(request, JobId):
	''' send a PICKCOMPLETE/PUTCOMPLETE message for job '''
	return redirect('/messagelocus/{}'.format(JobId))

@login_required
def sendcancelcomplete(request, JobId):
	''' send a CANCELCOMPLETE message for job '''
	job_data, job_type = get_job(JobId=JobId)
	send_request(request,job_data,job_type,"CANCELCOMPLETE")
	return redirect('/messagelocus/{}'.format(JobId))

@login_required
def sendcancelreject(request, JobId):
	''' send a CANCELREJECT message for job '''
	job_data, job_type = get_job(JobId=JobId)
	send_request(request,job_data,job_type,"CANCELREJECT","Rejected - Manually Posted")
	return redirect('/messagelocus/{}'.format(JobId))

@login_required
def sendupdatecomplete(request, JobId):
	''' send an UPDATECOMPLETE message for job '''
	job_data, job_type = get_job(JobId=JobId)
	send_request(request,job_data,job_type,"UPDATECOMPLETE")
	return redirect('/messagelocus/{}'.format(JobId))

@login_required
def sendupdatereject(request, JobId):
	''' send an UPDATEREJECT message for job '''
	job_data, job_type = get_job(JobId=JobId)
	send_request(request,job_data,job_type,"UPDATEREJECT","Rejected - Manually Posted")
	return redirect('/messagelocus/{}'.format(JobId))

@login_required
def sendtask(request, JobId):
	''' send a PICK/PUT message for job '''
	form_data = list(request.POST.items())
	task_data = {}
	for item in form_data[1:]:
		task_data[item[0][7:]] = item[1]

	job_data, job_type = get_job(JobId=JobId)

	if job_type == 'OrderJob':
		send_request(request,job_data,job_type,"PICK",None,task_data)
	elif job_type == 'PutawayJob':	
		send_request(request,job_data,job_type,"PUT",None,task_data)						
	return redirect('/messagelocus/{}'.format(JobId))