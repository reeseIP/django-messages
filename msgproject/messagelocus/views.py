# views.py
from django.db import IntegrityError
from django.contrib import messages
from django.shortcuts import get_object_or_404, render, redirect
from django.http import HttpResponse, HttpResponseRedirect
from django.forms import formset_factory
from django.views.decorators.csrf import csrf_exempt
from .models import OrderJobData, OrderTaskData, PutawayJobData, PutawayTaskData, ExternalUsers, ExternalSystems, OrderTaskResultData, PutawayTaskResultData, OrderJobEvents, PutawayJobEvents
from .forms import OrderTaskDataForm, PutawayTaskDataForm

from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.conf import settings

import json
import requests
import io
import base64
import datetime

# Create your views here.

### helper methods
def send_request(request,job_data,job_type,event_type=None,event_info=None,tasks=None):
	date = datetime.datetime.now().strftime(format='%Y-%m-%dT%H:%M:%S')
	if job_type == 'OrderJob':
		event_model = OrderJobEvents
		job_type = "OrderJobResult"
		job_message = {job_type: {"EventType":event_type,
											"EventInfo":event_info,
											"JobId":job_data["JobId"],
											"JobStatus":"Completed",
											"JobDate":date,
											"JobStation":None,
											"RequestId":job_data["RequestId"],
											"ToteId":job_data["ToteId"],
											"JobRobot":job_data['JobRobot'],
											"JobMethod":None,
											"JobTasks": tasks
											}}
	elif job_type == 'PutawayJob':
		event_model = PutawayJobEvents
		job_type = "PutawayJobResult"
		job_message = {job_type: {"EventType":event_type,
											"EventInfo":event_info,
											"LicensePlate":job_data['LicensePlate'],
											"RequestId":job_data['RequestId'],
											"JobId":job_data['JobId'],
											"JobDate":date,
											"JobStatus":'Completed',
											"JobStation":None,
											"JobRobot":job_data['JobRobot'],
											"JobTasks": tasks
											}}	
	elif job_type == 'PutawayRequest':
		event_model = None
		job_type = "PutawayJobRequest"
		job_message = {job_type: {"LicensePlate":job_data['LicensePlate'],
											"RequestDate":date,
											"RequestRobot":job_data['RequestRobot'],
											"RequestUser": request.user.username
											}}
	if event_model:
		# event entry
		event = event_model()
		event.JobId_id = job_data['id']
		event.EventType = event_type
		event.JobDate = date
		if event_type == 'PICK' or event_type == 'PUT':
			event.EventInfo = '{} Job: {} Task: {} Sent.'.format(event_type,job_data['JobId'],tasks[0]['JobTaskId'])
		else:
			event.EventInfo = '{} Job: {} Sent.'.format(event_type,job_data['JobId'])
		event.save()

	req_username = request.COOKIES['username']
	req_system = request.COOKIES['system']

	tar_user = ExternalUsers.objects.filter(username=req_username,system=req_system)[0]
	tar_sys = ExternalSystems.objects.filter(system=req_system)[0]

	if tar_user and tar_sys:
		client = requests.session()
		response = requests.post(tar_sys.url,
								json=job_message,
								auth=(tar_user.username,tar_user.password))

	# local testing
	#URL = http://127.0.0.1:8000
	#client.auth = (username,password)
	#response = client.post(URL,
	#						json=json.dumps(job_message))

	if response:
		if response.status_code == 200:
			messages.success(request, '{} {} sent!'.format(job_type,event_type))
		elif response.status_code != 200:
			messages.error(request, response.text)
	else:
		messages.error(request, 'Failed to send request')

def get_job(JobId):
	try:
		job = OrderJobData.objects.filter(JobId=JobId)[0]
		job_type = 'OrderJob'
	except IndexError:
		try:
			job = PutawayJobData.objects.filter(JobId=JobId)[0]
			job_type = 'PutawayJob'
		except IndexError:
			job = None
	
	if job:
		job_data = job.get_data()
		return {'job_query': job,
				'job_data':job_data, 
				'job_type':job_type}
	else:
		return None



### view methods
def index(request):
	return render(request, 'messagelocus/index.html')

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
	tar_sys_users = ExternalUsers.objects.filter(created_by=request.user).delete()
	logout(request)
	response = redirect('/messagelocus/login/')
	response.delete_cookie('username')
	response.delete_cookie('system')
	return response
	#return redirect('/messagelocus/login/')


@login_required
def active(request):
	''' landing page - list of jobs'''
	orders = OrderJobData.objects.filter(active=True).order_by('-JobId')[:]
	putaways = PutawayJobData.objects.filter(active=True).order_by('-JobId')[:]

	orderjob_list = []
	putawayjob_list = []

	for order in orders:
		event = OrderJobEvents.objects.filter(JobId=order).order_by('-JobDate')[0]
		orderjob_list.append({"JobId": order.JobId,
							  "latest_event": event.EventInfo})

	for putaway in putaways:
		event = PutawayJobEvents.objects.filter(JobId=putaway).order_by('-JobDate')[0]
		putawayjob_list.append({"JobId": putaway.JobId,
							    "latest_event": event.EventInfo})
		
	return render(request, 'messagelocus/active.html', {'orderjob_list': orderjob_list,
													   'putawayjob_list': putawayjob_list,
													  })

@login_required
def closed(request):
	''' landing page - list of jobs'''
	orders = OrderJobData.objects.filter(active=False).order_by('-JobId')[:]
	putaways = PutawayJobData.objects.filter(active=False).order_by('-JobId')[:]

	orderjob_list = []
	putawayjob_list = []

	for order in orders:
		event = OrderJobEvents.objects.filter(JobId=order).order_by('-JobDate')[0]
		orderjob_list.append({"JobId": order.JobId,
							  "latest_event": event.EventInfo})

	for putaway in putaways:
		event = PutawayJobEvents.objects.filter(JobId=putaway).order_by('-JobDate')[0]
		putawayjob_list.append({"JobId": putaway.JobId,
							    "latest_event": event.EventInfo})
		
	return render(request, 'messagelocus/closed.html', {'orderjob_list': orderjob_list,
													   'putawayjob_list': putawayjob_list,
													  })

@login_required
def close_job(request, JobId):
	''' close a job '''
	job = get_job(JobId=JobId)
	if job:
		job_query = job['job_query']
		job_query.active = False
		job_query.save()

	else:
		messages.error(request, 'Error occured when closing job')

	return redirect('/messagelocus/{}'.format(JobId))


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
			json_data = json.load(io.BytesIO(request.body))
			for k1, v1 in json_data.items():
				# outermost structure (Message Type)
				if k1 == 'OrderJob':
					job_model = OrderJobData
					task_model = OrderTaskData
					task_result_model = OrderTaskResultData
					event_model = OrderJobEvents
				elif k1 == 'PutawayJob':
					job_model = PutawayJobData
					task_model = PutawayTaskData
					task_result_model = PutawayTaskResultData
					event_model = PutawayJobEvents
				else:
					return HttpResponse('Error - Incorrect Message Type')

				job = get_job(JobId=v1['JobId'])
				
				if v1['EventType'] == 'NEW':
					if job:
						job_data = job['job_data']
						job_type = job['job_type']
						query = event_model.objects.filter(JobId_id=job_data['id'],EventType=v1['EventType'])
						if query:
							# job already exists
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
						new_job.active = True
						new_job.save()

						# new tasks
						job_tasks = v1['JobTasks']
						# task_type will be either OrderJobTask or PutawayJobTask for key
						# and a list of tasks for value
						for task_type, tasks in job_tasks.items():
							fields = task_model._meta.get_fields()
							result_fields = task_result_model._meta.get_fields()
							for task in tasks:
								new_task = task_model()
								new_result_task = task_result_model()
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
								for field in result_fields:
									if field.name == 'JobId':
										value = new_job
										setattr(new_result_task,field.name,value)
									elif field.name == 'ExecQty':
										value = task['TaskQty']
										setattr(new_result_task,field.name,value)
									else:
										try:
											value = task[field.name]
											if value == 'false':
												value = False 
											elif value == 'true':
												value = True
										except KeyError: # field was not supplied
											value = None
										setattr(new_result_task,field.name,value)

								new_task.save()
								new_result_task.save()

				# event entry
				event = event_model()
				if job:
					event.JobId = job['job_query']
					event.EventInfo = '{} Job: {} Requested.'.format(v1['EventType'],v1['JobId'])
				elif new_job:
					event.JobId = new_job
					event.EventInfo = '{} Job: {} Requested.'.format(v1['EventType'],v1['JobId'])
				event.EventType = v1['EventType']
				event.JobDate = v1['JobDate']
				event.save()

		else:
			return HttpResponse('Invalid Credentials')


		return HttpResponse('Ive Been hit')
	else:
		return HttpResponse('Inbound Request - GET')

@login_required
def jobview(request, JobId):
	''' overview for job details'''
	
	job = get_job(JobId=JobId)
	job_data = job['job_data']
	job_type = job['job_type']

	if job_type == 'OrderJob':
		TaskDataFormSet = formset_factory(OrderTaskDataForm, extra=0)
		tasks = OrderTaskResultData.objects.filter(JobId_id=job_data['id']).order_by('JobTaskId')[:]
		events = OrderJobEvents.objects.filter(JobId_id=job_data['id']).order_by('-JobDate')[:]
	elif job_type == 'PutawayJob':
		TaskDataFormSet = formset_factory(PutawayTaskDataForm, extra=0)
		tasks = PutawayTaskResultData.objects.filter(JobId_id=job_data['id']).order_by('JobTaskId')[:]
		events = PutawayJobEvents.objects.filter(JobId_id=job_data['id']).order_by('-JobDate')[:]

	job_events = []
	for event in events:
		job_events.append({'EventType':event.EventType,
							'JobDate':event.JobDate,
							'EventInfo':event.EventInfo})

	del job_data['id'] # dont want to pass this to the html template
	del job_data['active']
	
	task_data = []
	task_header = []
	
	for task in tasks:
		task_data.append(task.get_data())

	for item in task_data:
		del item['id']
		for key, value in item.items():
			setattr(task,key,value)
			task_header.append(key)
		
	formset = TaskDataFormSet(initial=task_data)

	task_header = list(dict.fromkeys(task_header))

	return render(request, "messagelocus/jobview.html", {'JobId': JobId,
														 'job_data': job_data,
														 'task_header': task_header,
														 'formset': formset,
														 'events': job_events,
														 })

@login_required
def putawayjobrequest(request):
	''' request a putawayjob from SAP system '''
	if request.method == 'GET':
		return render(request, "messagelocus/putawayjobrequest.html")
	elif request.method == 'POST':
		job_data = {'LicensePlate':request.POST['licenseplate'],
					'RequestRobot':request.POST['requestrobot'],}
		
		send_request(request,job_data,job_type='PutawayRequest')
		messages.success(request,'Putaway Job Requested')
		return redirect('/messagelocus/putawayjobrequest')


@login_required
def sendaccept(request, JobId):
	''' send an ACCEPT message for job '''
	job = get_job(JobId=JobId)
	job_data = job['job_data']
	job_type = job['job_type']
	send_request(request,job_data,job_type,"ACCEPT")
	return redirect('/messagelocus/{}'.format(JobId))

@login_required
def sendreject(request, JobId):
	''' send a REJECT message for job '''
	job = get_job(JobId=JobId)
	job_data = job['job_data']
	job_type = job['job_type']
	send_request(request,job_data,job_type,"REJECT","Rejected - Manually Posted")
	return redirect('/messagelocus/{}'.format(JobId))

@login_required
def sendinduct(request, JobId):
	''' send a TOTEINDUCT message for job '''
	job = get_job(JobId=JobId)
	job_data = job['job_data']
	job_type = job['job_type']
	job_query = job['job_query']
	if request.POST['robot']:
		job_query.JobRobot = request.POST['robot']
		job_query.save()
		job_data['JobRobot'] = request.POST['robot']
		if job_type == 'OrderJob':
			send_request(request,job_data,job_type,"TOTEINDUCT")
		elif job_type == 'PutawayJob':
			send_request(request,job_data,job_type,"PUTINDUCT")
	else:
		messages.error(request, 'Please enter a Robot')
	return redirect('/messagelocus/{}'.format(JobId))

@login_required
def sendcomplete(request, JobId):
	''' send a PICKCOMPLETE/PUTCOMPLETE message for job '''
	job = get_job(JobId=JobId)
	job_data = job['job_data']
	job_type = job['job_type']

	task_data = []
	if job_type == 'OrderJob':
		tasks = OrderTaskResultData.objects.filter(JobId_id=job_data['id'])
		for task in tasks:
			task_info = task.get_data()
			del task_info['id']
			task_data.append(task_info)
		send_request(request,job_data,job_type,"PICKCOMPLETE",None,tasks=task_data)
	elif job_type == 'PutawayJob':
		tasks = PutawayTaskResultData.objects.filter(JobId_id=job_data['id'])
		for task in tasks:
			task_info = task.get_data()
			del task_info['id']
			task_data.append(task_info)
		send_request(request,job_data,job_type,"PUTCOMPLETE",None,tasks=task_data)						
	return redirect('/messagelocus/{}'.format(JobId))

@login_required
def sendcancelcomplete(request, JobId):
	''' send a CANCELCOMPLETE message for job '''
	job = get_job(JobId=JobId)
	job_data = job['job_data']
	job_type = job['job_type']
	send_request(request,job_data,job_type,"CANCELCOMPLETE")
	return redirect('/messagelocus/{}'.format(JobId))

@login_required
def sendcancelreject(request, JobId):
	''' send a CANCELREJECT message for job '''
	job = get_job(JobId=JobId)
	job_data = job['job_data']
	job_type = job['job_type']
	send_request(request,job_data,job_type,"CANCELREJECT","Rejected - Manually Posted")
	return redirect('/messagelocus/{}'.format(JobId))

@login_required
def sendupdatecomplete(request, JobId):
	''' send an UPDATECOMPLETE message for job '''
	job = get_job(JobId=JobId)
	job_data = job['job_data']
	job_type = job['job_type']
	send_request(request,job_data,job_type,"UPDATECOMPLETE")
	return redirect('/messagelocus/{}'.format(JobId))

@login_required
def sendupdatereject(request, JobId):
	''' send an UPDATEREJECT message for job '''
	job = get_job(JobId=JobId)
	job_data = job['job_data']
	job_type = job['job_type']
	send_request(request,job_data,job_type,"UPDATEREJECT","Rejected - Manually Posted")
	return redirect('/messagelocus/{}'.format(JobId))

@login_required
def sendtask(request, JobId):
	''' send a PICK/PUT message for job '''
	form_data = list(request.POST.items())
	task_data = {}
	for item in form_data[1:]:
		task_data[item[0][7:]] = item[1]

	job = get_job(JobId=JobId)
	job_data = job['job_data']
	job_type = job['job_type']

	if job_type == 'OrderJob':
		send_request(request,job_data,job_type,"PICK",None,[task_data])
	elif job_type == 'PutawayJob':
		send_request(request,job_data,job_type,"PUT",None,[task_data])						
	return redirect('/messagelocus/{}'.format(JobId))

@login_required
def set_target_user(request):
	if request.method == 'POST':
		req_user = request.POST["username"] 
		req_syst = request.POST["system"]

		user = ExternalUsers.objects.filter(username=req_user,system=req_syst)[0]
		user = ExternalUsers()
		user.username = request.POST["username"] 
		user.password = request.POST["password"]
		user.csrf_token = request.POST["csrfmiddlewaretoken"]
		user.sessionid = request.POST["sessionid"]
		user.system = request.POST["system"]
		user.created_by = request.user
		try:
			user.save()
			return HttpResponse('Temporary User Created')
		except IntegrityError:
			#messages.error(request, 'Invalid User')
			return HttpResponse('Invalid User')