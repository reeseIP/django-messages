# models.py
from core.models import ModelHelp
from django.conf import settings
from django.contrib.auth.validators import UnicodeUsernameValidator
from django.db import models

# adding excluded fields to the django Model Meta class.  These fields will not be displayed in the app
# or considered for the message from the respective model
models.options.DEFAULT_NAMES = models.options.DEFAULT_NAMES + ('exclude_fields',)


''' Default Service Models '''
#---------------------------------------------------------------------#

class ExternalSystems(models.Model, ModelHelp):
	system  = models.CharField(max_length=3,null=False,primary_key=True)
	name 	= models.CharField(max_length=100)
	url     = models.CharField(max_length=250,null=False)

	def __str__(self):
		return('{}: {}'.format(self.system, self.url))

	def __repr__(self):
		return('{}: {}'.format(self.system, self.url))


class ExternalUsers(models.Model, ModelHelp):
	username_validator = UnicodeUsernameValidator()
	username   = models.CharField(
					("username"),
					max_length=150,
					help_text= (
						"Required. 150 characters or fewer. Letters, digits and @/./+/-/_ only."
					),
					validators=[username_validator],
				 )
	password   = models.CharField( ("password"), max_length=128)
	sessionid  = models.CharField(max_length=32,null=False)
	system 	   = models.ForeignKey(ExternalSystems, on_delete=models.CASCADE, related_name='users')
	created_by = models.ForeignKey(
			        settings.AUTH_USER_MODEL,
			        on_delete=models.CASCADE,
			        null=True
    			 )
	active     = models.BooleanField(default=False)

	def __str__(self):
		return('{}: {}'.format(self.system_id, self.username))

	def __repr__(self):
		return('{}: {}'.format(self.system_id, self.username))



''' Order Message Type Models '''
#---------------------------------------------------------------------#
class OrderJobs(models.Model, ModelHelp):
	#EventType  		 = models.CharField(max_length=50,blank=True,null=True,default='NEW')
	#EventInfo  		 = models.CharField(max_length=250,blank=True,null=True)
	JobId 			 = models.CharField(max_length=50)
	JobDate 		 = models.CharField(max_length=25)
	JobPriority 	 = models.CharField(max_length=10,blank=True,null=True)
	JobPriorityGroup = models.CharField(max_length=50,blank=True,null=True)
	RequestId 		 = models.CharField(max_length=50)
	ToteId			 = models.CharField(max_length=50)
	SingleUnit 		 = models.BooleanField(default=False,null=True)
	NextWorkArea 	 = models.CharField(max_length=50, blank=True, null=True)
	# additional fields
	JobRobot		 = models.CharField(max_length=50, blank=True, null=True)
	system 			 = models.ForeignKey(ExternalSystems, on_delete=models.CASCADE, related_name='orderjobs')
	active			 = models.BooleanField(default=True)

	class Meta:
		exclude_fields = [
			'id', # if no primary key is specified, this field is added as primary key
			'EventType',
			'EventInfo',
			'system',
			'active'
		]

	def __str__(self):
		return ('{}: {}'.format(self.system_id, self.JobId))

	def __repr__(self):
		return ('{}: {}'.format(self.system_id, self.JobId))


class OrderJobResults(models.Model, ModelHelp):
	EventType  = models.CharField(max_length=50)
	EventInfo  = models.CharField(max_length=250,blank=True,null=True)
	JobId 	   = models.CharField(max_length=50)
	JobStatus  = models.CharField(max_length=50, default='Completed')
	JobDate	   = models.CharField(max_length=25)
	JobStation = models.CharField(max_length=50,blank=True,null=True)
	RequestId  = models.CharField(max_length=50)
	ToteId	   = models.CharField(max_length=50)
	JobRobot   = models.CharField(max_length=50,blank=True,null=True)
	JobMethod  = models.CharField(max_length=50,blank=True,null=True)
	# additional fields
	Job 	   = models.ForeignKey(OrderJobs, on_delete=models.CASCADE, related_name='jobresults')
	#timestamp  = models.DateTimeField(auto_now=True)

	class Meta:
		exclude_fields = [
			'id',
			'Job_id',
			#'timestamp',
		]

	def save(self, *args, **kwargs):
		self.JobStatus = 'Completed'
		super().save(*args, **kwargs)

	#@classmethod
	#def get_last_result(cls,JobId):
	#	last_result = cls.objects.filter(JobId_id=JobId).order_by('-timestamp').first()
	#	return last_result

	def __str__(self):
		return('{}: {}'.format(self.JobId, self.EventType))

	def __repr__(self):
		return('{}: {}'.format(self.JobId, self.EventType))


class OrderTasks(models.Model, ModelHelp):
	JobTaskId 		   = models.CharField(max_length=50)
	EventAction		   = models.CharField(max_length=50,blank=True,null=True)
	OrderId 		   = models.CharField(max_length=50,blank=True,null=True)
	OrderLineId		   = models.CharField(max_length=50,blank=True,null=True)
	OrderTaskId 	   = models.CharField(max_length=50,blank=True,null=True)
	OrderType 		   = models.CharField(max_length=50,blank=True,null=True)
	CustOwner 		   = models.CharField(max_length=50,null=True)
	SiteId 			   = models.CharField(max_length=50,null=True)
	TaskType 		   = models.CharField(max_length=50)
	TaskSequence 	   = models.IntegerField(blank=True,null=True)
	TaskSubSequence	   = models.IntegerField(blank=True,null=True)
	TaskTravelPriority = models.IntegerField(blank=True,null=True)
	TaskLocation 	   = models.CharField(max_length=50)
	TaskZone 		   = models.CharField(max_length=50,blank=True,null=True)
	TaskWorkArea   	   = models.CharField(max_length=50,blank=True,null=True)
	TaskQty 		   = models.IntegerField()
	ItemNo 			   = models.CharField(max_length=50)
	ItemUPC 		   = models.CharField(max_length=50,blank=True,null=True)
	ItemDesc 		   = models.CharField(max_length=50,blank=True,null=True)
	ItemStyle 		   = models.CharField(max_length=50,blank=True,null=True)
	ItemColor 		   = models.CharField(max_length=50,blank=True,null=True)
	ItemSize 		   = models.CharField(max_length=50,blank=True,null=True)
	ItemLength 		   = models.DecimalField(max_digits=5,decimal_places=2,blank=True,null=True)
	ItemWidth 		   = models.DecimalField(max_digits=5,decimal_places=2,blank=True,null=True)
	ItemHeight 		   = models.DecimalField(max_digits=5,decimal_places=2,blank=True,null=True)
	ItemWeight 		   = models.DecimalField(max_digits=5,decimal_places=2,blank=True,null=True)
	ItemImageUrl 	   = models.CharField(max_length=250,blank=True)
	Custom1 		   = models.CharField(max_length=250,blank=True,null=True)
	Custom2 		   = models.CharField(max_length=250,blank=True,null=True)
	Custom3 		   = models.CharField(max_length=250,blank=True,null=True)
	Custom4 		   = models.CharField(max_length=250,blank=True,null=True)
	Custom5 		   = models.CharField(max_length=250,blank=True,null=True)
	Custom6 		   = models.CharField(max_length=250,blank=True,null=True)
	Custom7 		   = models.CharField(max_length=250,blank=True,null=True)
	Custom8 		   = models.CharField(max_length=250,blank=True,null=True)
	Custom9 		   = models.CharField(max_length=250,blank=True,null=True)
	Custom10 		   = models.CharField(max_length=250,blank=True,null=True)
	LotNo 			   = models.CharField(max_length=250,blank=True,null=True)
	SerialNo 		   = models.CharField(max_length=250,blank=True,null=True)
	CaptureLotNo 	   = models.BooleanField(default=False)
	CaptureSerialNo    = models.BooleanField(default=False)
	CaptureSerialNoQty = models.IntegerField(default=0)
	# additional fields
	Job 			   = models.ForeignKey(OrderJobs, on_delete=models.CASCADE, related_name='tasks')

	class Meta:
		exclude_fields = [
			'id',
			'Job_id'
		]

	def __str__(self):
		return ('{}: {}'.format(self.Job_id, self.JobTaskId))

	def __repr__(self):
		return ('{}: {}'.format(self.Job_id, self.JobTaskId))


class OrderTaskResults(models.Model, ModelHelp):
	JobTaskId 		= models.CharField(max_length=50)
	OrderId 		= models.CharField(max_length=50,blank=True,null=True)
	OrderLineId 	= models.CharField(max_length=50,blank=True,null=True)
	OrderTaskId 	= models.CharField(max_length=50,blank=True,null=True)
	CustOwner 		= models.CharField(max_length=50,null=True)
	SiteId 			= models.CharField(max_length=50,null=True)
	TaskStatus 		= models.CharField(max_length=50,blank=True,null=True)
	TaskType 		= models.CharField(max_length=50,blank=True,null=True)
	TaskLocation 	= models.CharField(max_length=50,blank=True,null=True)
	TaskQty 		= models.IntegerField()
	ExecQty 		= models.IntegerField()
	ExecUser 		= models.CharField(max_length=50)
	ExecDate 		= models.CharField(max_length=25)
	ExecRobot 		= models.CharField(max_length=50)
	ItemNo 			= models.CharField(max_length=50)
	ItemUPC 		= models.CharField(max_length=50,blank=True,null=True)
	ExceptionCode   = models.CharField(max_length=50,blank=True,null=True)
	ExceptionReason = models.CharField(max_length=50,blank=True,null=True)
	Custom1 		= models.CharField(max_length=250,blank=True,null=True)
	Custom2 		= models.CharField(max_length=250,blank=True,null=True)
	Custom3 		= models.CharField(max_length=250,blank=True,null=True)
	Custom4 		= models.CharField(max_length=250,blank=True,null=True)
	Custom5 		= models.CharField(max_length=250,blank=True,null=True)
	Custom6 		= models.CharField(max_length=250,blank=True,null=True)
	Custom7 		= models.CharField(max_length=250,blank=True,null=True)
	Custom8 		= models.CharField(max_length=250,blank=True,null=True)
	Custom9 		= models.CharField(max_length=250,blank=True,null=True)
	Custom10 		= models.CharField(max_length=250,blank=True,null=True)
	LotNo 			= models.CharField(max_length=250,blank=True,null=True)
	SerialNo 		= models.CharField(max_length=250,blank=True,null=True)
	# additional fields
	Job 			= models.ForeignKey(OrderJobs, on_delete=models.CASCADE, related_name='taskresults')
	#timestamp 		= models.DateTimeField(auto_now=True)


	class Meta:
		exclude_fields = [
			'id',
			'Job_id',
			#'timestamp',
		]

	#@classmethod
	#def get_last_task(cls,JobId,JobTaskId):
	#	''' get the data for the last task sent '''
	#	task = cls.objects.filter(JobId_id=JobId,JobTaskId=JobTaskId).order_by('-timestamp').first()
	#	return task

	def __str__(self):
		return ('{}: {}'.format(self.Job_id, self.JobTaskId))

	def __repr__(self):
		return ('{}: {}'.format(self.Job_id, self.JobTaskId))



''' Putaway Message Type Models '''
#---------------------------------------------------------------------#

class PutawayJobs(models.Model, ModelHelp):
	#EventType    = models.CharField(max_length=50,blank=True,null=True)
	#EventInfo    = models.CharField(max_length=250,blank=True,null=True)
	LicensePlate = models.CharField(max_length=50)
	RequestId 	 = models.CharField(max_length=50)
	JobId 		 = models.CharField(max_length=50)
	JobDate 	 = models.CharField(max_length=25)
	JobPriority  = models.CharField(max_length=10,blank=True,null=True)
	JobRobot	 = models.CharField(max_length=50, blank=True, null=True)
	# additional fields
	system 		 = models.ForeignKey(ExternalSystems, on_delete=models.CASCADE, related_name='putawayjobs')
	active 		 = models.BooleanField(default=True)

	class Meta:
		exclude_fields = [
			'id',
			'EventType',
			'EventInfo',
			'system',
			'active'
		]

	def __str__(self):
		return ('{}: {}'.format(self.system_id, self.JobId))

	def __repr__(self):
		return ('{}: {}'.format(self.system_id, self.JobId))


class PutawayJobResults(models.Model, ModelHelp):
	EventType 	 = models.CharField(max_length=50)
	EventInfo 	 = models.CharField(max_length=250,blank=True,null=True)
	LicensePlate = models.CharField(max_length=50)
	RequestId 	 = models.CharField(max_length=50)
	JobId 		 = models.CharField(max_length=50)
	JobDate 	 = models.CharField(max_length=25)
	JobStatus 	 = models.CharField(max_length=50, default='Completed')
	JobStation   = models.CharField(max_length=50,blank=True,null=True)
	JobRobot 	 = models.CharField(max_length=50,blank=True,null=True)
	# additional fields
	Job 		 = models.ForeignKey(PutawayJobs, on_delete=models.CASCADE, related_name='jobresults')
	#timestamp 	 = models.DateTimeField(auto_now=True)


	class Meta:
		exclude_fields = [
			'id',
			'Job_id',
			#'timestamp',
		]

	def save(self, *args, **kwargs):
		self.JobStatus = 'Completed'
		super().save(*args, **kwargs)

	#@classmethod
	#def get_last_result(cls,JobId):
	#	last_result = cls.objects.filter(JobId_id=JobId).order_by('-timestamp').first()
	#	return last_result

	def __str__(self):
		return('{}: {}'.format(self.JobId, self.EventType))

	def __repr__(self):
		return('{}: {}'.format(self.JobId, self.EventType))


class PutawayTasks(models.Model, ModelHelp):
	JobTaskId 		   = models.CharField(max_length=50)
	EventAction 	   = models.CharField(max_length=50,blank=True,null=True)
	InnerLicensePlate  = models.CharField(max_length=50,blank=True,null=True)
	OrderId 		   = models.CharField(max_length=50,blank=True,null=True)
	OrderLineId 	   = models.CharField(max_length=50,blank=True,null=True)
	OrderTaskId 	   = models.CharField(max_length=50,blank=True,null=True)
	OrderType 		   = models.CharField(max_length=50,blank=True,null=True)
	CustOwner 		   = models.CharField(max_length=50,null=True)
	SiteId 			   = models.CharField(max_length=50,null=True)
	TaskType 		   = models.CharField(max_length=50)
	TaskTravelPriority = models.IntegerField(blank=True,null=True)
	TaskLocation 	   = models.CharField(max_length=50)
	TaskZone 		   = models.CharField(max_length=50,blank=True,null=True)
	TaskWorkArea 	   = models.CharField(max_length=50,blank=True,null=True)
	TaskQty 		   = models.IntegerField()
	ItemNo 			   = models.CharField(max_length=50)
	ItemUPC 		   = models.CharField(max_length=50,blank=True,null=True)
	ItemDesc 		   = models.CharField(max_length=50,blank=True,null=True)
	ItemStyle	 	   = models.CharField(max_length=50,blank=True,null=True)
	ItemColor	 	   = models.CharField(max_length=50,blank=True,null=True)
	ItemSize 	 	   = models.CharField(max_length=50,blank=True,null=True)
	ItemLength 		   = models.DecimalField(max_digits=5, decimal_places=2,blank=True,null=True)
	ItemWidth 		   = models.DecimalField(max_digits=5, decimal_places=2,blank=True,null=True)
	ItemHeight 		   = models.DecimalField(max_digits=5, decimal_places=2,blank=True,null=True)
	ItemWeight 		   = models.DecimalField(max_digits=5, decimal_places=2,blank=True,null=True)
	ItemImageUrl 	   = models.CharField(max_length=250,blank=True)
	LotNo 			   = models.CharField(max_length=100,blank=True,null=True)
	SerialNo 		   = models.CharField(max_length=100,blank=True,null=True)
	Custom1 		   = models.CharField(max_length=250,blank=True,null=True)
	Custom2 		   = models.CharField(max_length=250,blank=True,null=True)
	Custom3 		   = models.CharField(max_length=250,blank=True,null=True)
	Custom4 		   = models.CharField(max_length=250,blank=True,null=True)
	Custom5 		   = models.CharField(max_length=250,blank=True,null=True)
	Custom6 		   = models.CharField(max_length=250,blank=True,null=True)
	Custom7 		   = models.CharField(max_length=250,blank=True,null=True)
	Custom8 		   = models.CharField(max_length=250,blank=True,null=True)
	Custom9 		   = models.CharField(max_length=250,blank=True,null=True)
	Custom10 		   = models.CharField(max_length=250,blank=True,null=True)
	# additional fields
	Job 			   = models.ForeignKey(PutawayJobs, on_delete=models.CASCADE, related_name='tasks')

	class Meta:
		exclude_fields = [
			'id',
			'Job_id',
		]

	def __str__(self):
		return ('{}: {}'.format(self.Job_id, self.JobTaskId))

	def __repr__(self):
		return ('{}: {}'.format(self.Job_id, self.JobTaskId))


class PutawayTaskResults(models.Model, ModelHelp):
	JobTaskId 		  = models.CharField(max_length=50)
	InnerLicensePlate = models.CharField(max_length=50,blank=True,null=True)
	OrderId 		  = models.CharField(max_length=50,blank=True,null=True)
	OrderLineId		  = models.CharField(max_length=50,blank=True,null=True)
	OrderTaskId 	  = models.CharField(max_length=50,blank=True,null=True)
	OrderType 		  = models.CharField(max_length=50,blank=True,null=True)
	CustOwner	 	  = models.CharField(max_length=50,null=True)
	SiteId 			  = models.CharField(max_length=50,null=True)
	TaskStatus 		  = models.CharField(max_length=50,blank=True,null=True)
	TaskType 		  = models.CharField(max_length=50)
	TaskLocation 	  = models.CharField(max_length=50)
	TaskQty 		  = models.IntegerField()
	ExecQty 		  = models.IntegerField()
	ExecUser 		  = models.CharField(max_length=50)
	ExecDate 		  = models.CharField(max_length=25)
	ExecRobot 		  = models.CharField(max_length=50)
	ItemNo 			  = models.CharField(max_length=50)
	LotNo 			  = models.CharField(max_length=100,blank=True,null=True)
	SerialNo 		  = models.CharField(max_length=100,blank=True,null=True)
	ExceptionCode 	  = models.CharField(max_length=50,blank=True,null=True)
	ExceptionReason   = models.CharField(max_length=50,blank=True,null=True)
	Custom1 		  = models.CharField(max_length=250,blank=True,null=True)
	Custom2 		  = models.CharField(max_length=250,blank=True,null=True)
	Custom3 		  = models.CharField(max_length=250,blank=True,null=True)
	Custom4 		  = models.CharField(max_length=250,blank=True,null=True)
	Custom5 		  = models.CharField(max_length=250,blank=True,null=True)
	Custom6			  = models.CharField(max_length=250,blank=True,null=True)
	Custom7 		  = models.CharField(max_length=250,blank=True,null=True)
	Custom8 		  = models.CharField(max_length=250,blank=True,null=True)
	Custom9 		  = models.CharField(max_length=250,blank=True,null=True)
	Custom10 		  = models.CharField(max_length=250,blank=True,null=True)
	# additional fields
	Job 			  = models.ForeignKey(PutawayJobs, on_delete=models.CASCADE, related_name='taskresults')
	#timestamp 		  = models.DateTimeField(auto_now=True)

	class Meta:
		exclude_fields = [
			'id',
			'Job_id',
			#'timestamp',
		]

	#@classmethod
	#def get_last_task(cls,JobId,JobTaskId):
	#	''' get the data for the last task sent '''
	#	task = cls.objects.filter(JobId_id=JobId,JobTaskId=JobTaskId).order_by('-timestamp').first()
	#	return task

	def __str__(self):
		return ('{}: {}'.format(self.Job_id, self.JobTaskId))

	def __repr__(self):
		return ('{}: {}'.format(self.Job_id, self.JobTaskId))



''' Event Models '''
#---------------------------------------------------------------------#

class OrderJobEvents(models.Model, ModelHelp):
	Job 	  = models.ForeignKey(OrderJobs, on_delete=models.CASCADE, related_name='events')
	EventType = models.CharField(max_length=50)
	JobDate   = models.CharField(max_length=25)
	EventInfo = models.CharField(max_length=250)
	payload   = models.TextField()
	#timestamp = models.DateTimeField(auto_now=True)

	class Meta:
		exclude_fields = [
			'id',
			'Job_id'
			#'timestamp',
			'payload',
		]

	@classmethod
	def get_last_event(cls,JobId):
		last_event = cls.objects.filter(JobId=JobId).order_by('-JobDate').first()
		return last_event

	def __str__(self):
		return('{}: {}'.format(self.Job_id, self.EventType))

	def __repr__(self):
		return('{}: {}'.format(self.Job_id, self.EventType))
	

class PutawayJobEvents(models.Model, ModelHelp):
	Job       = models.ForeignKey(PutawayJobs, on_delete=models.CASCADE, related_name='events')
	EventType = models.CharField(max_length=50)
	JobDate   = models.CharField(max_length=25)
	EventInfo = models.CharField(max_length=250)
	payload   = models.TextField()
	#timestamp = models.DateTimeField(auto_now=True)

	class Meta:
		exclude_fields = [
			'id',
			'Job_id'
			#'timestamp',
			'payload',
		]

	@classmethod
	def get_last_event(cls,JobId):
		last_event = cls.objects.filter(JobId=JobId).order_by('-JobDate').first()
		return last_event

	def __str__(self):
		return('{}: {}'.format(self.Job_id, self.EventType))

	def __repr__(self):
		return('{}: {}'.format(self.Job_id, self.EventType))


	
class OrderSerialNumbers(models.Model, ModelHelp):
	EventType   = models.CharField(max_length=50,default='SERIAL')
	JobId 	    = models.CharField(max_length=50)
	OrderId     = models.CharField(max_length=50,blank=True,null=True)
	OrderLineId = models.CharField(max_length=50,blank=True,null=True)
	JobTaskId   = models.CharField(max_length=50)
	ItemNo 	    = models.CharField(max_length=50)
	Quantity    = models.IntegerField(default=1)
	Serial      = models.CharField(max_length=128)
	# additional fields
	Job         = models.ForeignKey(OrderJobs, on_delete=models.CASCADE)
	JobTask     = models.ForeignKey(OrderTaskResults, on_delete=models.CASCADE, related_name='serialnumbers')
	
	class Meta:
		exclude_fields = [
			'id',
			'Job_id',
			'JobTask_id',
		]

	def __str__(self):
		return('{}: {}: {}'.format(self.JobId, self.JobTaskId, self.Serial))

	def __repr__(self):
		return('{}: {}: {}'.format(self.JobId, self.JobTaskId, self.Serial))

	def save(self, *args, **kwargs):
		self.Quantity = 1
		super().save(*args, **kwargs)


class PutawayJobRequests(models.Model, ModelHelp):
	LicensePlate = models.CharField(max_length=50)
	RequestDate  = models.CharField(max_length=25)
	RequestRobot = models.CharField(max_length=50,blank=True,null=True)
	RequestUser  = models.CharField(max_length=50,blank=True,null=True)

	class Meta:
		exclude_fields = [
			'id',
		]