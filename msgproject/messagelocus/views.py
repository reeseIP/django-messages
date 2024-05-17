# views.py
from django.contrib import messages
from django.contrib.auth import authenticate
from django.contrib.auth.decorators import login_required
from django.core.exceptions import ValidationError
from django.db import IntegrityError
from django.forms import formset_factory
from django.http import HttpResponse,JsonResponse
from django.shortcuts import render, redirect
from django.views.decorators.csrf import csrf_exempt
from django.core.signing import Signer

from .apps import MessagelocusConfig as app
from .forms import OrderTasksForm, PutawayTasksForm
from core.models import ExternalSystems, ExternalUsers
from .models import ( OrderJobs, OrderJobResults, OrderTasks, OrderTaskResults, OrderSerialNumbers, OrderJobEvents,
					  PutawayJobs, PutawayJobResults, PutawayTasks, PutawayTaskResults, PutawayJobEvents, PutawayJobRequests )

import base64
import datetime
import io
import json
import requests


''' global variables '''
#g_date = datetime.datetime.now().strftime(format='%Y-%m-%dT%H:%M:%S')
g_service = app.name


''' helper methods '''
#---------------------------------------------------------------------#
def send_request_basic(request, system, JobId, EventType, EventInfo=""):
	''' set basic result info and send request '''
	job = get_job(system, JobId)
	job_result = move_data(job['job_data'], job['job_result_model'])
	
	job_result.EventType = EventType
	job_result.EventInfo = EventInfo
	job_result.Job_id = job['job_query'].id
	job_result.JobDate = datetime.datetime.now().strftime(format='%Y-%m-%dT%H:%M:%S')#g_date

	send_request(request, system, job['result_type'], job_result)


def move_data(source, target, new_object=True):
	''' move data from a source dictionary to a target model '''
	fields = target.get_fields()
	if new_object:
		target = target()
	for field in fields:
		try:
			value = source[field]
			if value == 'false':
				value = False 
			elif value == 'true':
				value = True
		except KeyError: # field was not supplied
			value = None
		setattr(target,field,value)
	return target


def send_request(request, system, message_type, job, tasks=[]):
	''' send request to external system '''
	job_message = job.get_data()

	if message_type == 'OrderJobResult':
		event_model = OrderJobEvents
		job_message['JobTasks'] = [task.get_data() for task in tasks]
		job_message = {message_type: job_message}

	elif message_type == 'PutawayJobResult':
		event_model = PutawayJobEvents
		job_message['JobTasks'] = [task.get_data() for task in tasks]
		job_message = {message_type: job_message}

	elif message_type == 'PutawayJobRequest':
		event_model = None
		job_message = {message_type: job_message}

	elif message_type == 'SerialValidation':
		event_model = OrderJobEvents
	
	signer = Signer()

	ext_sys = ExternalSystems.objects.filter(system=system, service=g_service).first()
	ext_user = ext_sys.users.filter(created_by=request.user,active=True).first()
	ext_pass = signer.unsign_object(ext_user.password)

	if message_type == 'SerialValidation':
		index = ext_sys.url.find('?')
		ext_sys.url = ext_sys.url[:index] + '/validateSerial' + ext_sys.url[index:]

	if ext_user and ext_sys:
		#client = requests.session()
		response = requests.post(ext_sys.url,
								 json=job_message,
								 auth=(ext_user.username,ext_pass['password']))
	else:
		messages.error(request, 'A valid target user needs to be set before sending a request.')
		response = None

	if event_model:
		event = move_data(job.get_data(),event_model)
		event.Job_id = job.Job_id
		event.payload = str(job_message)
		event.JobDate = datetime.datetime.now().strftime(format='%Y-%m-%dT%H:%M:%S')#g_date
	else:
		event = None

	if response:
		if response.status_code == 200:
			if message_type == 'SerialValidation': 
				#event.EventType = 'SERIAL'
				event_info = 'Validating Serial Number {} for Task {}.'.format(job.Serial, job.JobTaskId)
			elif message_type == 'PutawayJobRequest': 
				event_info = '{} {} {} sent!'.format(message_type, job.LicensePlate, job.RequestRobot)
				messages.success(request, event_info)
			else:
				if job.EventType == 'PICK' or job.EventType == 'PUT':
					try:
						task = tasks[0].JobTaskId
					except IndexError:
						task = ''
					event_info = '{} {} Job: {} Task: {} Sent.'.format(message_type, job.EventType, job.JobId, task)
				else:
					event_info = '{} {} Job: {} Sent.'.format(message_type, job.EventType, job.JobId)	
				messages.success(request, event_info)		
		else:
			event_info = 'Failed to send request. HTTP status code: {}'.format(response.status_code)
			messages.error(request, event_info)

	else:
		event_info = 'Failed to send request'
		messages.error(request, event_info)

	if event:
		#event.EventType = event_type
		event.EventInfo = event_info
		event.save()

	if message_type != 'SerialValidation':
		job.save()
		[task.save() for task in tasks]

	return response


def get_job(system, JobId):
	''' get job and assign default attributes '''
	try:
		job = OrderJobs.objects.filter(JobId=JobId, system_id__system=system)[0]
		job_type = 'OrderJob'
		result_type = 'OrderJobResult'
		job_model = OrderJobs
		task_model = OrderTasks
		job_result_model = OrderJobResults
		task_result_model = OrderTaskResults
		event_model = OrderJobEvents
		
	except IndexError:
		try:
			job = PutawayJobs.objects.filter(JobId=JobId, system_id__system=system)[0]
			job_type = 'PutawayJob'
			result_type = 'PutawayJobResult'
			job_model = PutawayJobs
			task_model = PutawayTasks
			job_result_model = PutawayJobResults
			task_result_model = PutawayTaskResults
			event_model = PutawayJobEvents
		except IndexError:
			job = None
	
	if job:
		job_data = job.get_data()
		return {'job_query'         : job,
				'job_data'          : job_data, 
				'job_type'          : job_type,
				'result_type'       : result_type,
				'job_model'         : job_model,
				'task_model'        : task_model,
				'job_result_model'  : job_result_model,
				'task_result_model' : task_result_model,
				'event_model'		: event_model}
	else:
		return None



''' view handler methods '''
#---------------------------------------------------------------------#
def index(request):
	''' home page '''
	return render(request, 'messagelocus/index.html')


@login_required
def active(request, system):
	''' active jobs '''
	system = ExternalSystems.objects.filter(system=system, service=g_service).first()
	orders = system.orderjobs.filter(active=True)#.order_by('-JobId')
	putaways = system.putawayjobs.filter(active=True)

	orderjob_list = []
	putawayjob_list = []

	for order in orders:
		event = order.events.order_by('-JobDate').first()
		order_data = order.get_data()
		if event:
			order_data['Latest Event'] = event.EventInfo
		else:
			order_data['Latest Event'] = ''
		orderjob_list.append(order_data)

	for putaway in putaways:
		event = putaway.events.order_by('-JobDate').first()
		putaway_data = putaway.get_data()
		keyorder = ['JobId', 'JobDate', 'JobPriority', 'RequestId', 'LicensePlate', 'JobRobot']
		[keyorder.append(field) for field in putaway_data if field != 'JobId']
		putaway_data = {k: putaway_data[k] for k in keyorder if k in putaway_data}
		if event:
			putaway_data['Latest Event'] = event.EventInfo
		else:
			putaway_data['Latest Event'] = ''
		putawayjob_list.append(putaway_data)

	orderjob_fields = OrderJobs.get_fields()
	putawayjob_fields = PutawayJobs.get_fields()

	# change the sort order of putaway fields
	keyorder = ['JobId', 'JobDate', 'JobPriority', 'RequestId', 'LicensePlate', 'JobRobot']
	[keyorder.append(field) for field in putawayjob_fields if field != 'JobId']
	
	putawayjob_fields = {k: putawayjob_fields[k] for k in keyorder if k in putawayjob_fields}

	orderjob_fields = list(orderjob_fields.keys())
	putawayjob_fields = list(putawayjob_fields.keys())

	orderjob_fields.append('Latest Event')
	putawayjob_fields.append('Latest Event')

	try:
		theme = request.COOKIES['theme']
	except KeyError:
		theme = 'light'
		
	return render(request, 'messagelocus/active.html', {'orderjob_list': orderjob_list,
														'orderjob_fields': orderjob_fields,
													   	'putawayjob_list': putawayjob_list,
													   	'putawayjob_fields': putawayjob_fields,
													  	'theme': theme
													  })


@login_required
def closed(request, system):
	''' closed jobs'''
	system = ExternalSystems.objects.filter(system=system, service=g_service).first()
	orders = system.orderjobs.filter(active=False)#.order_by('-JobId')
	putaways = system.putawayjobs.filter(active=False)

	orderjob_list = []
	putawayjob_list = []

	for order in orders:
		event = order.events.order_by('-JobDate').first()
		order_data = order.get_data()
		if event:
			order_data['Latest Event'] = event.EventInfo
		else:
			order_data['Latest Event'] = ''
		orderjob_list.append(order_data)

	for putaway in putaways:
		event = putaway.events.order_by('-JobDate').first()
		putaway_data = putaway.get_data()
		keyorder = ['JobId', 'JobDate', 'JobPriority', 'RequestId', 'LicensePlate', 'JobRobot']
		[keyorder.append(field) for field in putaway_data if field != 'JobId']
		putaway_data = {k: putaway_data[k] for k in keyorder if k in putaway_data}
		if event:
			putaway_data['Latest Event'] = event.EventInfo
		else:
			putaway_data['Latest Event'] = ''
		putawayjob_list.append(putaway_data)

	orderjob_fields = OrderJobs.get_fields()
	putawayjob_fields = PutawayJobs.get_fields()

	# change the sort order of putaway fields
	keyorder = ['JobId', 'JobDate', 'JobPriority', 'RequestId', 'LicensePlate', 'JobRobot']
	[keyorder.append(field) for field in putawayjob_fields if field != 'JobId']
	
	putawayjob_fields = {k: putawayjob_fields[k] for k in keyorder if k in putawayjob_fields}

	orderjob_fields = list(orderjob_fields.keys())
	putawayjob_fields = list(putawayjob_fields.keys())

	orderjob_fields.append('Latest Event')
	putawayjob_fields.append('Latest Event')

	try:
		theme = request.COOKIES['theme']
	except KeyError:
		theme = 'light'
		
	return render(request, 'messagelocus/closed.html', {'orderjob_list': orderjob_list,
														'orderjob_fields': orderjob_fields,
													   	'putawayjob_list': putawayjob_list,
													   	'putawayjob_fields': putawayjob_fields,
													   	'theme': theme
													  })


@login_required
def jobview(request, system, JobId):
	''' overview for job details'''
	job = get_job(system, JobId)

	if job['job_type'] == 'OrderJob':
		TaskDataFormSet = formset_factory(OrderTasksForm, extra=0)
	elif job['job_type'] == 'PutawayJob':
		TaskDataFormSet = formset_factory(PutawayTasksForm, extra=0)
	
	tasks = job['job_query'].tasks.order_by('JobTaskId').all()
	formset = TaskDataFormSet(initial=[move_data(task.get_data(), job['task_result_model']).get_data() for task in tasks])

	events = job['job_query'].events.order_by('-JobDate').all()
	job_events = [event.get_data() for event in events]

	try:
		theme = request.COOKIES['theme']
	except KeyError:
		theme = 'light'
	
	return render(request, "messagelocus/jobview.html", {'JobId': JobId,
														 'job_data': job['job_data'],
														 'job_type': job['job_type'],
														 'task_header': job['task_result_model'].get_fields(),
														 'formset': formset,
														 'events': job_events,
														 'theme': theme,
														 'active': job['job_query'].active
														 })


''' javascript event handler methods '''
#---------------------------------------------------------------------#
@login_required
def putawayjobrequest(request, system):
	''' request a putawayjob from external system '''
	if request.method == 'POST':
		put_request = PutawayJobRequests()
		put_request.LicensePlate = request.POST['licenseplate']
		put_request.RequestRobot = request.POST['requestrobot']
		
		send_request(request, system, 'PutawayJobRequest', put_request)
		#if response.status_code == 200:
		#	messages.success(request,'Putaway Job Requested')
		return JsonResponse({'status_code':response.status_code})


@login_required
def sendaccept(request, system, JobId):
	''' send an ACCEPT message for job '''
	if request.method == 'POST':
		send_request_basic(request, system, JobId, 'ACCEPT')
	return redirect('/messagelocus/{}/{}/'.format(system, JobId))


@login_required
def sendreject(request, system, JobId):
	''' send a REJECT message for job '''
	if request.method == 'POST':
		send_request_basic(request, system, JobId, 'REJECT', 'Rejected - Manually Rejected')
	return redirect('/messagelocus/{}/{}/'.format(system, JobId))


@login_required
def sendinduct(request, system, JobId):
	''' send a TOTEINDUCT message for job '''
	if request.method == 'POST':
		job = get_job(system, JobId)
		job['job_query'].JobRobot = request.POST['robot']
		job['job_query'].save()

		if job['job_type'] == 'OrderJob':
			send_request_basic(request, system, JobId, 'TOTEINDUCT')
		elif job['job_type'] == 'PutawayJob':
			send_request_basic(request, system, JobId, 'PUTINDUCT')
	return redirect('/messagelocus/{}/{}/'.format(system, JobId))


@login_required
def sendcomplete(request, system, JobId):
	''' send a PICKCOMPLETE/PUTCOMPLETE message for job '''
	if request.method == 'POST':
		job = get_job(system, JobId)

		tasks = [task for task in job['job_query'].taskresults.all()]
		if job['job_type'] == 'OrderJob':
			event_type = 'PICKCOMPLETE'
			for task in tasks:
				task.SerialNo = [serial.Serial for serial in task.serialnumbers.all()]

		elif job['job_type'] == 'PutawayJob':
			event_type = 'PUTCOMPLETE'

		job_result = move_data(job['job_data'], job['job_result_model'])
		job_result.EventType = event_type
		job_result.Job_id = job['job_query'].id
		job_result.JobDate = datetime.datetime.now().strftime(format='%Y-%m-%dT%H:%M:%S')#g_date	

		send_request(request, system, job['result_type'], job_result, tasks)

	return redirect('/messagelocus/{}/{}/'.format(system,JobId))


@login_required
def sendcancelcomplete(request, system, JobId):
	''' send a CANCELCOMPLETE message for job '''
	if request.method == 'POST':
		send_request_basic(request, system, JobId, 'CANCELCOMPLETE')
	return redirect('/messagelocus/{}/{}/'.format(system, JobId))


@login_required
def sendcancelreject(request, system, JobId):
	''' send a CANCELREJECT message for job '''
	if request.method == 'POST':
		send_request_basic(request, system, JobId, 'CANCELREJECT', 'Rejected - Manually Rejected')
	return redirect('/messagelocus/{}/{}/'.format(system, JobId))


@login_required
def sendupdatecomplete(request, system, JobId):
	''' send an UPDATECOMPLETE message for job '''
	if request.method == 'POST':
		send_request_basic(request, system, JobId, 'UPDATECOMPLETE')
	return redirect('/messagelocus/{}/{}/'.format(system, JobId))


@login_required
def sendupdatereject(request, system, JobId):
	''' send an UPDATEREJECT message for job '''
	if request.method == 'POST':
		send_request_basic(request, system, JobId, 'UPDATEREJECT', 'Rejected - Manually Rejected')
	return redirect('/messagelocus/{}/{}/'.format(system, JobId))


@login_required
def sendtask(request, system, JobId, JobTaskId):
	''' send a PICK/PUT message for job '''
	if request.method == 'POST':
		task_data = {}
		serial_buffer = []
		serial_numbers = []
		form_data = list(request.POST.items())

		job = get_job(system, JobId)
		job_query = job['job_query']

		if job['job_type'] == 'OrderJob':
			event_type = 'PICK'

		elif job['job_type'] == 'PutawayJob':
			event_type = 'PUT'

		try:
			for item in form_data[1:]:
				if item[0][0:2] == 'SN':
					serial_numbers.append(item[1])
				else:
					# data in for is formatted form-X-fieldname, parse off form-X-
					index = len(item[0])
					index_of_dash = item[0].rfind('-', 0, index)
					task_data[item[0][index_of_dash+1:]] = item[1]

			try:
				job_result = move_data(job['job_data'], job['job_result_model'])
				job_result.EventType = event_type
				job_result.Job_id = job_query.id
				job_result.JobDate = datetime.datetime.now().strftime(format='%Y-%m-%dT%H:%M:%S')#g_date
				job_result.save()

				# update task
				task = job_query.taskresults.filter(JobTaskId=JobTaskId).first()
				if task:
					task_result = move_data(task_data, task, new_object=False)
				else: 
					task_result = move_data(task_data, job['task_result_model'])

				task_result.Job_id = job_query.id
				task_result.ExecDate = datetime.datetime.now().strftime(format='%Y-%m-%dT%H:%M:%S')#g_date
				if serial_numbers:
					task_result.SerialNo = serial_numbers
				task_result.save()
				
				for serial in serial_numbers:
					new_serial = move_data(task_result.get_data(), OrderSerialNumbers)
					new_serial.EventType = 'SERIAL'
					new_serial.JobId = job_query.JobId
					new_serial.Job_id = job_query.id
					new_serial.JobTask_id = task_result.id
					new_serial.Serial = serial
					serial_buffer.append(new_serial)

				[serial.save() for serial in serial_buffer]

				send_request(request, system, job['result_type'], job_result, [task_result])

			except (ValidationError, ValueError):
				if job_result.id:
					job_result.delete()
				messages.error(request, 'Failed to send task.')
			
		except IndexError:
			messages.error(request, 'Failed to read task data.')

	return redirect('/messagelocus/{}/{}/'.format(system,JobId))


@login_required
def sendprint(request, system, JobId):
	''' send print request '''
	if request.method == 'POST':
		send_request_basic(request, system, JobId, 'PRINT', 'LOCL')
	return redirect('/messagelocus/{}/{}/'.format(system, JobId))


@login_required
def get_active_users(request, system):
	''' get active external user '''
	if request.method == 'POST':
		user = ExternalUsers.objects.filter(created_by=request.user,system=system,sessionid=request.COOKIES['sessionid'],active=True).first()
		if user:
			user = user.username
		return JsonResponse({'user': user})


@login_required
def get_capture_field_data(request, system, JobId, JobTaskId):
	''' get the amount of required serial numbers for input '''
	if request.method == 'POST':
		job = get_job(system, JobId)
		#JobTaskId = request.POST['JobTaskId']
		serial_numbers = []

		if job['job_type'] == 'OrderJob':
			task_obj = job['job_query'].tasks.filter(JobTaskId=JobTaskId).first()
			var_ser_qty = task_obj.CaptureSerialNoQty

				#task_obj = OrderTaskResults.get_last_task(JobId=JobId,JobTaskId=JobTaskId)
				#serial_obj = OrderSerialNumbers.objects.filter(JobTaskId_id=task_obj.id)
				#if serial_obj:
				#	for obj in serial_obj:
				#		serial_numbers.append(obj.SerialNo)
		else:
			var_ser_qty = 0

		return JsonResponse({'SerialQty': var_ser_qty,
							 'SerialNumbers': serial_numbers})


@login_required
def validate_serial_number(request, system, JobId, JobTaskId):
	''' validate a serial number against an external system '''
	if request.method == 'POST':

		job = OrderJobs.objects.filter(JobId=JobId,system_id__system=system).first()
		task_data = job.tasks.filter(JobTaskId=JobTaskId).first().get_data()

		serial_val = move_data(task_data, OrderSerialNumbers)
		serial_val.EventType = 'SERIAL'
		serial_val.JobId = JobId
		serial_val.Quantity = 1
		serial_val.Serial = request.POST['SerialNumber']
		serial_val.Job_id = job.id

		response = send_request(request, system, 'SerialValidation', serial_val)
		#response_data = json.loads(response.text)
		
		return JsonResponse({'status_code': response.status_code,
							 		'data': json.loads(response.text)})


@login_required
def close_job(request, system, JobId):
	''' close job '''
	if request.method == 'POST':
		job = get_job(system, JobId)

		if job:
			job['job_query'].active = False
			job['job_query'].save()
			messages.success(request, 'Job {} Closed'.format(job['job_query'].JobId))
			response = {'status_code': 200}
		else:
			messages.error(request, 'Error occured when closing job')
			response = {'status_code': 500}

		return JsonResponse(response)


@login_required
def check_job_exists(request, system):
	''' check if job exists in given system '''
	if request.method == 'POST':
		orderjob = OrderJobs.objects.filter(JobId=request.POST['search'],system_id__system=system)
		putawayjob = PutawayJobs.objects.filter(JobId=request.POST['search'],system_id__system=system)

		if not orderjob and not putawayjob:
			return JsonResponse({'status_code': 500})
		else:
			return JsonResponse({'status_code': 200})


''' API destination methods '''
#---------------------------------------------------------------------#


@csrf_exempt
def inbound_xml(request, system):
	print(request.body)
	return HttpResponse('inbound_xml')

@csrf_exempt
def inbound(request, system):
	''' inbound messages '''
	if request.method == 'POST':
		# validate the requested system
		system_query = ExternalSystems.objects.filter(system__iexact=system, service=g_service).first()
		if not system_query:
			return HttpResponse('system exists not')
		auth_header = request.META['HTTP_AUTHORIZATION']
		try:
			encoded_credentials = auth_header.split(' ')[1] # Removes "Basic " to isolate credentials
			decoded_credentials = base64.b64decode(encoded_credentials).decode("utf-8").split(':')
			username, password = decoded_credentials[0], decoded_credentials[1]
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
					event_model = OrderJobEvents

				elif k1 == 'PutawayJob':
					job_model = PutawayJobs
					task_model = PutawayTasks
					event_model = PutawayJobEvents
				else:
					return HttpResponse('Error - Incorrect Message Type')

				job = get_job(system, v1['JobId'])
				
				if v1['EventType'] == 'NEW':
					if job:
						job_result = move_data(job['job_data'], job['job_result_model'])
						job_result.Job_id = job['job_query'].id
						job_result.EventType = 'REJECT'
						job_result.EventInfo = "Rejected - Job Already Exists"
						job_result.JobDate = datetime.datetime.now().strftime(format='%Y-%m-%dT%H:%M:%S')#g_date
						return HttpResponse(send_request(request, system, job['result_type'], job_result))
					else:
						try:
							new_job = move_data(v1, job_model)
							new_job.system_id = system_query.id
							new_job.active = True
							new_job.save()

							job_tasks = v1['JobTasks']
							job_tasks_buff = []

							''' task_type will be either OrderJobTask or PutawayJobTask for key
							 and a list of tasks for value'''
							for task_type, tasks in job_tasks.items():
								for task in tasks:
									''' new task '''
									new_task = move_data(task, task_model)
									new_task.Job_id = new_job.id

									job_tasks_buff.append(new_task)

						
							[task.save() for task in job_tasks_buff]
						except (ValidationError, ValueError) as e:
							if new_job.id:
								new_job.delete()
							return HttpResponse(e)

				new_event = move_data(v1, event_model)
				if job:
					new_event.Job_id = job.id
				else:
					new_event.Job_id = new_job.id
				new_event.EventInfo = '{} Job: {} Requested.'.format(v1['EventType'],v1['JobId'])
				new_event.payload = request.body.decode('utf-8')
				new_event.save()
					
				return HttpResponse('Job Successfully Created')

		else:
			return HttpResponse('Invalid Credentials')



