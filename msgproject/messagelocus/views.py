# views.py
from django.db import IntegrityError
from django.contrib import messages
from django.shortcuts import get_object_or_404, render, redirect
from django.http import HttpResponse, HttpResponseRedirect, JsonResponse
from django.forms import formset_factory
from django.views.decorators.csrf import csrf_exempt
from .forms import OrderTasksForm, PutawayTasksForm
from .models import ( OrderJobs, OrderTasks, OrderTaskResults, OrderSerialNumbers, OrderJobEvents,
					PutawayJobs, PutawayTasks, PutawayTaskResults, PutawayJobEvents,
					ExternalUsers, ExternalSystems )

from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.conf import settings

import json
import requests
import io
import base64
import datetime


### helper methods
def send_request(request,job_data,job_type,event_type="",event_info="",tasks="",serial_number=""):
	date = datetime.datetime.now().strftime(format='%Y-%m-%dT%H:%M:%S')
	if job_type == 'OrderJob':
		event_model = OrderJobEvents
		job_type = "OrderJobResult"
		job_message = {job_type: {"EventType":event_type,
											"EventInfo":event_info,
											"JobId":job_data["JobId"],
											"JobStatus":"Completed",
											"JobDate":date,
											"JobStation":'',
											"RequestId":job_data["RequestId"],
											"ToteId":job_data["ToteId"],
											"JobRobot":job_data['JobRobot'],
											"JobMethod":'',
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
											"JobStation":'',
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
	elif job_type == 'SerialValidation':
		event_model = OrderJobEvents
		job_message = {"EventType": event_type,
						"JobId": job_data["JobId"],
						"OrderId": tasks['OrderId'],
						"OrderLineId": tasks['OrderLineId'],
						"JobTaskId": tasks['JobTaskId'],
						"ItemNo": tasks['ItemNo'],
						"Quantity": '1',
						"Serial": serial_number}

	try:
		req_username = request.COOKIES['username']
		req_system = request.COOKIES['system']
	except KeyError:
		messages.error(request, 'A valid target user needs to be set before sending a request.')
		return


	tar_user = ExternalUsers.objects.filter(username=req_username,system=req_system).first()
	tar_sys = ExternalSystems.objects.filter(system=req_system).first()

	if job_type == 'SerialValidation':
		index = tar_sys.url.find('?')
		tar_sys.url = tar_sys.url[:index] + '/validateSerial' + tar_sys.url[index:]

	if tar_user and tar_sys:
		#client = requests.session()
		response = requests.post(tar_sys.url,
								json=job_message,
								auth=(tar_user.username,tar_user.password))
	else:
		messages.error(request, 'A valid target user needs to be set before sending a request.')
		return

	# local testing
	#URL = http://127.0.0.1:8000
	#client.auth = (username,password)
	#response = client.post(URL,
	#						json=json.dumps(job_message))

	if response:
		if response.status_code == 200:
			if event_type != 'SERIAL':
				messages.success(request, '{} {} sent!'.format(job_type,event_type))
			if event_model:
				# event entry
				event = event_model()
				event.JobId_id = job_data['id']
				event.EventType = event_type
				event.JobDate = date
				if event_type == 'PICK' or event_type == 'PUT':
					try:
						task = tasks[0]['JobTaskId']
					except IndexError:
						task = ''
					event.EventInfo = '{} Job: {} Task: {} Sent.'.format(event_type,job_data['JobId'],task)
				elif event_type != 'SERIAL':
					event.EventInfo = '{} Job: {} Sent.'.format(event_type,job_data['JobId'])
				event.save()
		elif response.status_code != 200:
			messages.error(request, response.text)
	else:
		messages.error(request, 'Failed to send request')

	return response


def get_job(JobId):
	try:
		job = OrderJobs.objects.filter(JobId=JobId)[0]
		job_type = 'OrderJob'
	except IndexError:
		try:
			job = PutawayJobs.objects.filter(JobId=JobId)[0]
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
	return redirect('/messagelocus/active/')

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

@login_required
def active(request):
	''' landing page - list of jobs'''
	orders = OrderJobs.objects.filter(active=True).order_by('-JobId').all()
	putaways = PutawayJobs.objects.filter(active=True).order_by('-JobId').all()

	orderjob_list = []
	putawayjob_list = []

	for order in orders:
		event = OrderJobEvents.objects.filter(JobId=order).order_by('-JobDate').first()
		order_data = order.get_data()
		if event:
			order_data['Latest Event'] = event.EventInfo
		else:
			order_data['Latest Event'] = ''
		orderjob_list.append(order_data)

	for putaway in putaways:
		event = PutawayJobEvents.objects.filter(JobId=putaway).order_by('-JobDate').first()
		putaway_data = putaway.get_data()
		keyorder = ['JobId']
		[keyorder.append(field) for field in putaway_data if field != 'JobId']
		putaway_data = {k: putaway_data[k] for k in keyorder if k in putaway_data}
		if event:
			putaway_data['Latest Event'] = event.EventInfo
		else:
			putaway_data['Latest Event'] = ''
		putawayjob_list.append(putaway_data)

	orderjob_fields = OrderJobs.get_fields()
	putawayjob_fields = PutawayJobs.get_fields()

	# dont pass these to the html doc
	del orderjob_fields['id']
	del orderjob_fields['active']
	del putawayjob_fields['id']
	del putawayjob_fields['active']

	# change the sort order of putaway fields
	keyorder = ['JobId']
	[keyorder.append(field) for field in putawayjob_fields if field != 'JobId']
	
	putawayjob_fields = {k: putawayjob_fields[k] for k in keyorder if k in putawayjob_fields}

	orderjob_fields = list(orderjob_fields.keys())
	putawayjob_fields = list(putawayjob_fields.keys())

	orderjob_fields.append('Latest Event')
	putawayjob_fields.append('Latest Event')


		
	return render(request, 'messagelocus/active.html', {'orderjob_list': orderjob_list,
														'orderjob_fields': orderjob_fields,
													   'putawayjob_list': putawayjob_list,
													   'putawayjob_fields': putawayjob_fields,
													  })

@login_required
def closed(request):
	''' landing page - list of jobs'''
	orders = OrderJobs.objects.filter(active=False).order_by('-JobId').all()
	putaways = PutawayJobs.objects.filter(active=False).order_by('-JobId').all()

	orderjob_list = []
	putawayjob_list = []

	for order in orders:
		event = OrderJobEvents.objects.filter(JobId=order).order_by('-JobDate').first()
		orderjob_list.append({"JobId": order.JobId,
							  "latest_event": event.EventInfo})

	for putaway in putaways:
		event = PutawayJobEvents.objects.filter(JobId=putaway).order_by('-JobDate').first()
		putawayjob_list.append({"JobId": putaway.JobId,
							    "latest_event": event.EventInfo})
		
	return render(request, 'messagelocus/closed.html', {'orderjob_list': orderjob_list,
													   'putawayjob_list': putawayjob_list,
													  })

@login_required
def close_job(request):
	''' close a job '''
	job = get_job(request.POST['JobId'])
	if job:
		job_query = job['job_query']
		job_query.active = False
		job_query.save()
		messages.success(request, 'Job {} Closed'.format(job.JobId))

	else:
		messages.error(request, 'Error occured when closing job')

	return redirect('/messagelocus/{}'.format(request.POST['JobId']))


@csrf_exempt
def inbound(request):
	''' inbound messages '''
	if request.method == 'POST':
		auth_header = request.META['HTTP_AUTHORIZATION']
		try:
			encoded_credentials = auth_header.split(' ')[1] # Removes "Basic " to isolate credentials
			decoded_credentials = base64.b64decode(encoded_credentials).decode("utf-8").split(':')
			username = decoded_credentials[0]
			password = decoded_credentials[1]
		except IndexError:
			return HttpResponse('Invalid Credentials')

		user = authenticate(request, username=username, password=password)
		if user is not None:
			json_data = json.load(io.BytesIO(request.body))
			for k1, v1 in json_data.items():
				# outermost structure (Message Type)
				if k1 == 'OrderJob':
					job_model = OrderJobs
					task_model = OrderTasks
					task_result_model = OrderTaskResults
					event_model = OrderJobEvents
				elif k1 == 'PutawayJob':
					job_model = PutawayJobs
					task_model = PutawayTasks
					task_result_model = PutawayTaskResults
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

								print(new_task)
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

				return HttpResponse('Job Successfully Created')

		else:
			return HttpResponse('Invalid Credentials')


@login_required
def jobview(request, JobId):
	''' overview for job details'''
	job = get_job(JobId=JobId)
	job_data = job['job_data']
	job_type = job['job_type']

	if job_type == 'OrderJob':
		task_model = OrderTaskResults
		event_model = OrderJobEvents
		TaskDataFormSet = formset_factory(OrderTasksForm, extra=0)
	elif job_type == 'PutawayJob':
		task_model = PutawayTaskResults
		event_model =PutawayJobEvents
		TaskDataFormSet = formset_factory(PutawayTasksForm, extra=0)

	tasks = task_model.objects.filter(JobId_id=job_data['id']).order_by('JobTaskId').all()
	events = event_model.objects.filter(JobId_id=job_data['id']).order_by('-JobDate').all()
	
	job_events = []
	for event in events:
		job_events.append({'EventType':event.EventType,
							'JobDate':event.JobDate,
							'EventInfo':event.EventInfo})	
	task_data = []

	d = {x.JobTaskId: x for x in tasks}
	mylist = list(d.values())

	for task in mylist:
		last_task = task_model.get_last_task(job_data['id'],task.JobTaskId)
		task_data.append(last_task.get_data())

	formset = TaskDataFormSet(initial=task_data)
	
	task_header = task_model.get_fields()
	# keep hidden on page
	del task_header['id'] 
	del task_header['timestamp']
	
	return render(request, "messagelocus/jobview.html", {'JobId': JobId,
														 'job_data': job_data,
														 'job_type': job_type,
														 'task_header': task_header,
														 'formset': formset,
														 'events': job_events,
														 })

@login_required
def putawayjobrequest(request):
	''' request a putawayjob from SAP system '''
	if request.method == 'POST':
		job_data = {'LicensePlate':request.POST['licenseplate'],
					'RequestRobot':request.POST['requestrobot'],}
		
		response = send_request(request,job_data,job_type='PutawayRequest')
		if response.status_code == 200:
			messages.success(request,'Putaway Job Requested')
		return JsonResponse({'status_code':response.status_code})


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
	job_query.JobRobot = request.POST['robot']
	job_query.save()
	job_data['JobRobot'] = request.POST['robot']
	if job_type == 'OrderJob':
		send_request(request,job_data,job_type,"TOTEINDUCT")
	elif job_type == 'PutawayJob':
		send_request(request,job_data,job_type,"PUTINDUCT")
	return redirect('/messagelocus/{}'.format(JobId))

@login_required
def sendcomplete(request, JobId):
	''' send a PICKCOMPLETE/PUTCOMPLETE message for job '''
	job = get_job(JobId=JobId)
	job_data = job['job_data']
	job_type = job['job_type']

	serial_numbers = []

	serial_query = OrderSerialNumbers.objects.filter(JobId_id=job['job_query'].id)

	task_data = []
	if job_type == 'OrderJob':
		tasks = OrderTaskResults.objects.filter(JobId_id=job_data['id']).all()

		d = {x.JobTaskId: x for x in tasks}
		mylist = list(d.values())

		for task in mylist:
			last_task = OrderTaskResults.get_last_task(job_data['id'],task.JobTaskId)
			last_task_data = last_task.get_data()
			for serial in serial_query:
				if last_task_data['id'] == serial.JobTaskId_id:
					serial_numbers.append(serial.SerialNo)
			if serial_numbers:
				last_task_data['SerialNo'] = serial_numbers.copy()
			del last_task_data['id']
			del last_task_data['timestamp']
			task_data.append(last_task_data)
			serial_numbers.clear()
			del last_task_data
		send_request(request,job_data,job_type,"PICKCOMPLETE",'',tasks=task_data)
	elif job_type == 'PutawayJob':
		tasks = PutawayTaskResults.objects.filter(JobId_id=job_data['id'])
		for task in tasks:
			task_info = task.get_data()
			del task_info['id']
			del task_info['timestamp']
			task_data.append(task_info)
		send_request(request,job_data,job_type,"PUTCOMPLETE",'',tasks=task_data)						
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
	serial_numbers = []

	try:
		for item in form_data[1:]:
			if item[0][0:2] == 'SN':
				# capture serial numbers
				serial_numbers.append(item[1])
			else:
				# data in for is formatted form-X-fieldname, parse off form-X-
				index = len(item[0])
				index_of_dash = item[0].rfind('-', 0, index)
				task_data[item[0][index_of_dash+1:]] = item[1]

		if serial_numbers:
			task_data['SerialNo'] = serial_numbers

		job = get_job(JobId=JobId)
		job_data = job['job_data']
		job_type = job['job_type']

		if job_type == 'OrderJob':
			new_task = OrderTaskResults()
			response = send_request(request,job_data,job_type,"PICK",None,[task_data])
		elif job_type == 'PutawayJob':
			new_task = PutawayTaskResults()
			response = send_request(request,job_data,job_type,"PUT",None,[task_data])	

		if response.status_code	== 200:
			# update the job data in the DB to capture the additional data sent
			for key, value in task_data.items():
				setattr(new_task,key,value)
		
			new_task.JobId_id = job_data['id']
			new_task.save()
		
			for item in serial_numbers:
				new_serial = OrderSerialNumbers()
				new_serial.JobId_id = job_data['id']
				new_serial.JobTaskId_id = new_task.id
				new_serial.SerialNo = item
				new_serial.save()
	except IndexError:
		messages.error(request, 'Failed to read task data.')

	return redirect('/messagelocus/{}'.format(JobId))


@login_required
def sendprint(request,JobId):
	job = get_job(JobId=JobId)
	job_data = job['job_data']
	job_type = job['job_type']
	send_request(request,job_data,job_type,"PRINT","LOCL")
	return redirect('/messagelocus/{}'.format(JobId))


@login_required
def set_target_user(request):
	if request.method == 'POST':
		req_user = request.POST["username"] 
		req_syst = request.POST["system"]

		user = ExternalUsers.objects.filter(username=req_user,system=req_syst).first()
		if user:
			messages.info(request, 'User Already Valid')
			return JsonResponse({'status_code': 200})
		else:
			tar_sys = ExternalSystems.objects.filter(system=req_syst).first()
			# validate user is valid in external system
			response = requests.get(tar_sys.url,
										auth=(request.POST["username"],request.POST["password"]))
			if response:
				if response.status_code == 200:
					user = ExternalUsers()
					user.username = request.POST["username"] 
					user.password = request.POST["password"]
					user.csrf_token = request.POST["csrfmiddlewaretoken"]
					user.sessionid = request.POST["sessionid"]
					user.system = request.POST["system"]
					user.created_by = request.user
					try:
						user.save()
						messages.success(request, 'Temporary User {} Created'.format(user.username))
						return JsonResponse({'status_code': 200})
					except IntegrityError:
						pass
				
			messages.error(request, 'Invalid User')
			return JsonResponse({'status_code': 500})

@login_required
def get_capture_field_data(request):
	JobId = request.POST['JobId']
	JobTaskId = request.POST['JobTaskId']
	serial_numbers = []

	task_obj = OrderTasks.objects.filter(JobTaskId=JobTaskId).first()
	if task_obj:
		var_ser_qty = task_obj.CaptureSerialNoQty

		task_obj = OrderTaskResults.get_last_task(JobId=JobId,JobTaskId=JobTaskId)
		serial_obj = OrderSerialNumbers.objects.filter(JobTaskId_id=task_obj.id)
		if serial_obj:
			for obj in serial_obj:
				serial_numbers.append(obj.SerialNo)
	else:
		var_ser_qty = 0
		serial_numbers = []

	return JsonResponse({'SerialQty': var_ser_qty,
						 'SerialNumbers': serial_numbers})


@login_required
def validate_serial_number(request):
	if request.method == 'POST':
		return JsonResponse({'status_code':500,
							 })
		job_data = OrderJobs.objects.filter(id=request.POST['JobId']).first().get_data()
		task_data = OrderTaskResults.get_last_task(JobId=request.POST['JobId'],JobTaskId=request.POST['JobTaskId']).get_data()
		response = send_request(request,job_data=job_data,job_type='SerialValidation',event_type='SERIAL',event_info=None,tasks=task_data,serial_number=request.POST['SerialNumber'])
		response_data = json.loads(response.text)
		return JsonResponse({'status_code':response.status_code,
							 'data': response_data})


@login_required
def check_job_exists(request):
	orderjob = OrderJobs.objects.filter(JobId=request.POST['search'])
	putawayjob = PutawayJobs.objects.filter(JobId=request.POST['search'])
	print(putawayjob)

	if not orderjob and not putawayjob:
		return JsonResponse({'status_code': 500})
	else:
		return JsonResponse({'status_code': 200})

@login_required
def delete_target_user(request):
	entry = ExternalUsers.objects.filter(username=request.POST['username'],
												system=request.POST['system'],
												created_by=request.user)
	if entry.delete()[1]:
		messages.success(request,'User successfully deleted.')
	else:
		messages.error(request,'Unable to delete user.')

	return JsonResponse({'status_code': 200})