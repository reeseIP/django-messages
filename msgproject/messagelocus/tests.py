from django.test import Client, TestCase
from django.contrib.auth.models import User
from .models import ( OrderJobs, OrderTasks, OrderTaskResults, OrderSerialNumbers, OrderJobEvents,
					PutawayJobs, PutawayTasks, PutawayTaskResults, PutawayJobEvents,
					ExternalUsers, ExternalSystems )

import base64
import json

# Create your tests here.

# login
# logout

class TestMessageLocus(TestCase):
	@classmethod
	def setUpTestData(cls):
		cls.client = Client()

	def test_user_registration(self):
		response = self.client.post('/messagelocus/register/', {'username': 'testuser', 'email':'test@user.com', 'password1': '89ao8sdhfa98shdp9gahsd', 'password2': '89ao8sdhfa98shdp9gahsd'})
		user = User.objects.filter(username='testuser').first()
		self.assertRedirects(response, '/messagelocus/active/', status_code=302, 
        target_status_code=200, fetch_redirect_response=False)
		self.assertEqual(user.username, 'testuser')

	def test_inbound_orderjob_single_task(self):
		self.client.post('/messagelocus/register/', {'username': 'testuser', 'email':'test@user.com', 'password1': '89ao8sdhfa98shdp9gahsd', 'password2': '89ao8sdhfa98shdp9gahsd'})
		credentials = base64.b64encode(b'testuser:89ao8sdhfa98shdp9gahsd').decode('utf-8')
		self.client.defaults['HTTP_AUTHORIZATION'] = 'Basic ' + credentials
		job_message = {"OrderJob":{"EventType":"NEW","JobId":"EDB1900001","JobDate":"2023-11-11T00:53:52","JobPriority":"002","JobPriorityGroup":"2023-11-11T00:53:52","RequestId":"900001","ToteId":"1100000000001146","JobTasks":{"OrderJobTask":[{"JobTaskId":"Z00001","EventAction":"","OrderId":"4400009047","OrderLineId":"0000000010","OrderTaskId":"","CustOwner":"","SiteId":"EDB1","TaskType":"PICK","TaskLocation":"01-10-01-02","TaskZone":"","TaskQty":1,"ItemNo":"78426963","ItemUPC":"","ItemDesc":"FA/PLUS GRANULE-DOG 650GM","ItemStyle":"","ItemColor":"","ItemSize":"","ItemLength":0,"ItemWidth":1,"ItemHeight":1,"ItemWeight":2,"ItemImageUrl":"","Custom1":"","Custom2":"","Custom3":"","Custom4":"","Custom5":"","Custom6":"","Custom7":"","Custom8":"","Custom9":"","Custom10":"","LotNo":"","SerialNo":"","CaptureLotNo":"false","CaptureSerialNo":"false","CaptureSerialNoQty":"0"}]}}}
		response = self.client.post('/messagelocus/inbound/', data=json.dumps(job_message), content_type='application/json')
		job = OrderJobs.objects.filter(JobId='EDB1900001').first()
		task = OrderTasks.objects.filter(JobId_id=job.id)
		task_result = OrderTaskResults.objects.filter(JobId_id=job.id)
		self.assertEqual(job.JobId, 'EDB1900001')
		self.assertEqual(len(task), 1)
		self.assertEqual(len(task_result), 1)
		
	def test_inbound_orderjob_multi_task(self):
		self.client.post('/messagelocus/register/', {'username': 'testuser', 'email':'test@user.com', 'password1': '89ao8sdhfa98shdp9gahsd', 'password2': '89ao8sdhfa98shdp9gahsd'})
		credentials = base64.b64encode(b'testuser:89ao8sdhfa98shdp9gahsd').decode('utf-8')
		self.client.defaults['HTTP_AUTHORIZATION'] = 'Basic ' + credentials
		job_message = {"OrderJob":{"EventType":"NEW","JobId":"EDB1900002","JobDate":"2023-11-11T00:53:52","JobPriority":"002","JobPriorityGroup":"2023-11-11T00:53:52","RequestId":"900002","ToteId":"1100000000001147","JobTasks":{"OrderJobTask":[{"JobTaskId":"Z00002","EventAction":"","OrderId":"4400009048","OrderLineId":"0000000010","OrderTaskId":"","CustOwner":"","SiteId":"EDB1","TaskType":"PICK","TaskLocation":"04-50-04-03","TaskZone":"","TaskQty":1,"ItemNo":"78426963","ItemUPC":"","ItemDesc":"FA/PLUS GRANULE-DOG 650GM","ItemStyle":"","ItemColor":"","ItemSize":"","ItemLength":0,"ItemWidth":1,"ItemHeight":1,"ItemWeight":2,"ItemImageUrl":"","Custom1":"","Custom2":"","Custom3":"","Custom4":"","Custom5":"","Custom6":"","Custom7":"","Custom8":"","Custom9":"","Custom10":"","LotNo":"","SerialNo":"","CaptureLotNo":"false","CaptureSerialNo":"false","CaptureSerialNoQty":"0"},{"JobTaskId":"Z00003","EventAction":"","OrderId":"4400009048","OrderLineId":"0000000010","OrderTaskId":"","CustOwner":"","SiteId":"EDB1","TaskType":"PICK","TaskLocation":"04-50-04-03","TaskZone":"","TaskQty":1,"ItemNo":"78426963","ItemUPC":"","ItemDesc":"FA/PLUS GRANULE-DOG 650GM","ItemStyle":"","ItemColor":"","ItemSize":"","ItemLength":0,"ItemWidth":1,"ItemHeight":1,"ItemWeight":2,"ItemImageUrl":"","Custom1":"","Custom2":"","Custom3":"","Custom4":"","Custom5":"","Custom6":"","Custom7":"","Custom8":"","Custom9":"","Custom10":"","LotNo":"","SerialNo":"","CaptureLotNo":"false","CaptureSerialNo":"false","CaptureSerialNoQty":"false"}]}}}
		response = self.client.post('/messagelocus/inbound/', data=json.dumps(job_message), content_type='application/json')
		job = OrderJobs.objects.filter(JobId='EDB1900002').first()
		task = OrderTasks.objects.filter(JobId_id=job.id)
		task_result = OrderTaskResults.objects.filter(JobId_id=job.id)
		self.assertEqual(job.JobId, 'EDB1900002')
		self.assertEqual(len(task), 2)
		self.assertEqual(len(task_result), 2)


	def test_inbound_putawayjob_single_task(self):
		self.client.post('/messagelocus/register/', {'username': 'testuser', 'email':'test@user.com', 'password1': '89ao8sdhfa98shdp9gahsd', 'password2': '89ao8sdhfa98shdp9gahsd'})
		credentials = base64.b64encode(b'testuser:89ao8sdhfa98shdp9gahsd').decode('utf-8')
		self.client.defaults['HTTP_AUTHORIZATION'] = 'Basic ' + credentials
		job_message = {"PutawayJob":{"EventType":"NEW","EventInfo":"","LicensePlate":"1100000000001144","RequestId":"100001","JobId":"EDB1100001","JobDate":"2023-11-11T00:53:52","JobPriority":"000","JobTasks":{"PutawayJobTask":[{"JobTaskId":"A00001","EventAction":"","InnerLicensePlate":"","OrderId":"4400009045","OrderLineId":"0000000010","OrderTaskId":"","OrderType":"","CustOwner":"3011","SiteId":"EDB1","TaskType":"PUT","TaskTravelPriority":0,"TaskLocation":"12-32-23-03","TaskZone":"","TaskWorkArea":"","TaskQty":1,"ItemNo":"78426963","ItemUPC":"","ItemDesc":"FA/PLUS GRANULE-DOG 650GM","ItemStyle":"","ItemColor":"","ItemSize":"","ItemLength":0,"ItemWidth":1,"ItemHeight":1,"ItemWeight":2,"ItemImageUrl":"","LotNo":"","SerialNo":"","Custom1":"","Custom2":"","Custom3":"","Custom4":"","Custom5":"","Custom6":"","Custom7":"","Custom8":"","Custom9":"","Custom10":""}]}}}
		response = self.client.post('/messagelocus/inbound/', data=json.dumps(job_message), content_type='application/json')
		job = PutawayJobs.objects.filter(JobId='EDB1100001').first()
		task = PutawayTasks.objects.filter(JobId_id=job.id)
		task_result = PutawayTaskResults.objects.filter(JobId_id=job.id)
		self.assertEqual(job.JobId, 'EDB1100001')
		self.assertEqual(len(task), 1)
		self.assertEqual(len(task_result), 1)

	def test_inbound_putawayjob_multi_task(self):
		self.client.post('/messagelocus/register/', {'username': 'testuser', 'email':'test@user.com', 'password1': '89ao8sdhfa98shdp9gahsd', 'password2': '89ao8sdhfa98shdp9gahsd'})
		credentials = base64.b64encode(b'testuser:89ao8sdhfa98shdp9gahsd').decode('utf-8')
		self.client.defaults['HTTP_AUTHORIZATION'] = 'Basic ' + credentials
		job_message = {"PutawayJob":{"EventType":"NEW","EventInfo":"","LicensePlate":"1100000000001145","RequestId":"100002","JobId":"EDB1100002","JobDate":"2023-11-11T00:53:52","JobPriority":"000","JobTasks":{"PutawayJobTask":[{"JobTaskId":"A00002","EventAction":"","InnerLicensePlate":"","OrderId":"4400009046","OrderLineId":"0000000010","OrderTaskId":"","OrderType":"","CustOwner":"3011","SiteId":"EDB1","TaskType":"PUT","TaskTravelPriority":0,"TaskLocation":"43-23-20-06","TaskZone":"","TaskWorkArea":"","TaskQty":1,"ItemNo":"78426963","ItemUPC":"","ItemDesc":"FA/PLUS GRANULE-DOG 650GM","ItemStyle":"","ItemColor":"","ItemSize":"","ItemLength":0,"ItemWidth":1,"ItemHeight":1,"ItemWeight":2,"ItemImageUrl":"","LotNo":"","SerialNo":"","Custom1":"","Custom2":"","Custom3":"","Custom4":"","Custom5":"","Custom6":"","Custom7":"","Custom8":"","Custom9":"","Custom10":""},{"JobTaskId":"A00003","EventAction":"","InnerLicensePlate":"","OrderId":"4400009049","OrderLineId":"0000000010","OrderTaskId":"","OrderType":"","CustOwner":"3011","SiteId":"EDB1","TaskType":"PUT","TaskTravelPriority":0,"TaskLocation":"GR-CONS","TaskZone":"","TaskWorkArea":"","TaskQty":1,"ItemNo":"78426963","ItemUPC":"","ItemDesc":"FA/PLUS GRANULE-DOG 650GM","ItemStyle":"","ItemColor":"","ItemSize":"","ItemLength":0,"ItemWidth":1,"ItemHeight":1,"ItemWeight":2,"ItemImageUrl":"","LotNo":"","SerialNo":"","Custom1":"","Custom2":"","Custom3":"","Custom4":"","Custom5":"","Custom6":"","Custom7":"","Custom8":"","Custom9":"","Custom10":""}]}}}
		response = self.client.post('/messagelocus/inbound/', data=json.dumps(job_message), content_type='application/json')
		job = PutawayJobs.objects.filter(JobId='EDB1100002').first()
		task = PutawayTasks.objects.filter(JobId_id=job.id)
		task_result = PutawayTaskResults.objects.filter(JobId_id=job.id)
		self.assertEqual(job.JobId, 'EDB1100002')
		self.assertEqual(len(task), 2)
		self.assertEqual(len(task_result), 2)