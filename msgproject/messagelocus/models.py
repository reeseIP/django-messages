# models.py
from django.db import models
from django.conf import settings
from django.contrib.auth.validators import UnicodeUsernameValidator

### helper methods
def hlp_get_data(obj_inst):
	data = {}
	fields = obj_inst._meta.get_fields()
	for field in fields:
		if 'Field' in type(field).__name__:
			attr = getattr(obj_inst,field.name)
			if attr == None:
				attr = ''
			data[field.name] = attr
	return(data)


class OrderJobs(models.Model):
	JobId = models.CharField(max_length=50)
	JobDate = models.CharField(max_length=25)
	JobPriority = models.CharField(max_length=10,blank=True,null=True)
	JobPriorityGroup = models.CharField(max_length=50,blank=True,null=True)
	RequestId = models.CharField(max_length=50)
	ToteId = models.CharField(max_length=50)
	SingleUnit = models.BooleanField(default=False,null=True)
	NextWorkArea = models.CharField(max_length=50, blank=True, null=True)
	JobRobot = models.CharField(max_length=50, blank=True, null=True)
	active = models.BooleanField(default=True)

	def __str__(self):
		return self.JobId

	def __repr__(self):
		return self.JobId

	def get_data(self):
		return hlp_get_data(self)


class OrderTasks(models.Model):
	JobId = models.ForeignKey(OrderJobs, on_delete=models.CASCADE)
	JobTaskId = models.CharField(max_length=50)
	EventAction = models.CharField(max_length=50,blank=True,null=True)
	OrderId = models.CharField(max_length=50,blank=True,null=True)
	OrderLineId = models.CharField(max_length=50,blank=True,null=True)
	OrderTaskId = models.CharField(max_length=50,blank=True,null=True)
	OrderType = models.CharField(max_length=50,blank=True,null=True)
	CustOwner = models.CharField(max_length=50,null=True)
	SiteId = models.CharField(max_length=50,null=True)
	TaskType = models.CharField(max_length=50)
	TaskSequence = models.IntegerField(blank=True,null=True)
	TaskSubSequence = models.IntegerField(blank=True,null=True)
	TaskTravelPriority = models.IntegerField(blank=True,null=True)
	TaskLocation = models.CharField(max_length=50)
	TaskZone = models.CharField(max_length=50,blank=True,null=True)
	TaskWorkArea = models.CharField(max_length=50,blank=True,null=True)
	TaskQty = models.IntegerField()
	ItemNo = models.CharField(max_length=50)
	ItemUPC = models.CharField(max_length=50,blank=True,null=True)
	ItemDesc = models.CharField(max_length=50)
	ItemStyle = models.CharField(max_length=50,blank=True,null=True)
	ItemColor = models.CharField(max_length=50,blank=True,null=True)
	ItemSize = models.CharField(max_length=50,blank=True,null=True)
	ItemLength = models.DecimalField(max_digits=5,decimal_places=2,blank=True,null=True)
	ItemWidth = models.DecimalField(max_digits=5,decimal_places=2,blank=True,null=True)
	ItemHeight = models.DecimalField(max_digits=5,decimal_places=2,blank=True,null=True)
	ItemWeight = models.DecimalField(max_digits=5,decimal_places=2,blank=True,null=True)
	ItemImageUrl = models.CharField(max_length=250,blank=True)
	Custom1 = models.CharField(max_length=250,blank=True,null=True)
	Custom2 = models.CharField(max_length=250,blank=True,null=True)
	Custom3 = models.CharField(max_length=250,blank=True,null=True)
	Custom4 = models.CharField(max_length=250,blank=True,null=True)
	Custom5 = models.CharField(max_length=250,blank=True,null=True)
	Custom6 = models.CharField(max_length=250,blank=True,null=True)
	Custom7 = models.CharField(max_length=250,blank=True,null=True)
	Custom8 = models.CharField(max_length=250,blank=True,null=True)
	Custom9 = models.CharField(max_length=250,blank=True,null=True)
	Custom10 = models.CharField(max_length=250,blank=True,null=True)
	LotNo = models.CharField(max_length=250,blank=True,null=True)
	SerialNo = models.CharField(max_length=250,blank=True,null=True)
	CaptureLotNo = models.BooleanField(default=False)
	CaptureSerialNo = models.BooleanField(default=False)
	CaptureSerialNoQty = models.IntegerField(default=0)

	def __str__(self):
		return self.JobTaskId

	def __repr__(self):
		return self.JobTaskId

	def get_data(self):
		return hlp_get_data(self)


class OrderTaskResults(models.Model):
	JobId = models.ForeignKey(OrderJobs, on_delete=models.CASCADE)
	JobTaskId = models.CharField(max_length=50)
	OrderId = models.CharField(max_length=50,blank=True,null=True)
	OrderLineId = models.CharField(max_length=50,blank=True,null=True)
	OrderTaskId = models.CharField(max_length=50,blank=True,null=True)
	CustOwner = models.CharField(max_length=50,null=True)
	SiteId = models.CharField(max_length=50,null=True)
	TaskStatus = models.CharField(max_length=50,blank=True,null=True)
	TaskType = models.CharField(max_length=50,blank=True,null=True)
	TaskLocation = models.CharField(max_length=50,blank=True,null=True)
	TaskQty = models.IntegerField()
	ExecQty = models.IntegerField(blank=True,null=True)
	ExecUser = models.CharField(max_length=50,blank=True,null=True)
	ExecDate = models.CharField(max_length=25,blank=True,null=True)
	ExecRobot = models.CharField(max_length=50,blank=True,null=True)
	ItemNo = models.CharField(max_length=50)
	ItemUPC = models.CharField(max_length=50,blank=True,null=True)
	ExceptionCode = models.CharField(max_length=50,blank=True,null=True)
	ExceptionReason = models.CharField(max_length=50,blank=True,null=True)
	Custom1 = models.CharField(max_length=250,blank=True,null=True)
	Custom2 = models.CharField(max_length=250,blank=True,null=True)
	Custom3 = models.CharField(max_length=250,blank=True,null=True)
	Custom4 = models.CharField(max_length=250,blank=True,null=True)
	Custom5 = models.CharField(max_length=250,blank=True,null=True)
	Custom6 = models.CharField(max_length=250,blank=True,null=True)
	Custom7 = models.CharField(max_length=250,blank=True,null=True)
	Custom8 = models.CharField(max_length=250,blank=True,null=True)
	Custom9 = models.CharField(max_length=250,blank=True,null=True)
	Custom10 = models.CharField(max_length=250,blank=True,null=True)
	LotNo = models.CharField(max_length=250,blank=True,null=True)
	SerialNo = models.CharField(max_length=250,blank=True,null=True)
	timestamp = models.DateTimeField(auto_now=True)

	@classmethod
	def get_last_task(cls,JobId,JobTaskId):
		''' get the data for the last task sent '''
		tasks = cls.objects.filter(JobId_id=JobId,JobTaskId=JobTaskId).order_by('-timestamp')
		return tasks[0]

	def __str__(self):
		return ('{}: {}'.format(self.id, self.JobTaskId))

	def __repr__(self):
		return ('{}: {}'.format(self.id, self.JobTaskId))

	def get_data(self):
		return hlp_get_data(self)


class PutawayJobs(models.Model):
	LicensePlate = models.CharField(max_length=50)
	RequestId = models.CharField(max_length=50)
	JobId = models.CharField(max_length=50)
	JobDate = models.CharField(max_length=25)
	JobPriority = models.CharField(max_length=10,blank=True,null=True)
	JobRobot = models.CharField(max_length=50, blank=True, null=True)
	active = models.BooleanField(default=True)

	def __str__(self):
		return self.JobId

	def __repr__(self):
		return self.JobId

	def get_data(self):
		return hlp_get_data(self)


class PutawayTasks(models.Model):
	JobId = models.ForeignKey(PutawayJobs, on_delete=models.CASCADE)
	JobTaskId = models.CharField(max_length=50)
	EventAction = models.CharField(max_length=50,blank=True,null=True)
	InnerLicensePlate = models.CharField(max_length=50,blank=True,null=True)
	OrderId = models.CharField(max_length=50,blank=True,null=True)
	OrderLineId = models.CharField(max_length=50,blank=True,null=True)
	OrderTaskId = models.CharField(max_length=50,blank=True,null=True)
	OrderType = models.CharField(max_length=50,blank=True,null=True)
	CustOwner = models.CharField(max_length=50,null=True)
	SiteId = models.CharField(max_length=50,null=True)
	TaskType = models.CharField(max_length=50)
	TaskTravelPriority = models.IntegerField(blank=True,null=True)
	TaskLocation = models.CharField(max_length=50)
	TaskZone = models.CharField(max_length=50,blank=True,null=True)
	TaskWorkArea = models.CharField(max_length=50,blank=True,null=True)
	TaskQty = models.IntegerField()
	ItemNo = models.CharField(max_length=50)
	ItemUPC = models.CharField(max_length=50,blank=True,null=True)
	ItemDesc = models.CharField(max_length=50)
	ItemStyle = models.CharField(max_length=50,blank=True,null=True)
	ItemColor = models.CharField(max_length=50,blank=True,null=True)
	ItemSize = models.CharField(max_length=50,blank=True,null=True)
	ItemLength = models.DecimalField(max_digits=5, decimal_places=2,blank=True,null=True)
	ItemWidth = models.DecimalField(max_digits=5, decimal_places=2,blank=True,null=True)
	ItemHeight = models.DecimalField(max_digits=5, decimal_places=2,blank=True,null=True)
	ItemWeight = models.DecimalField(max_digits=5, decimal_places=2,blank=True,null=True)
	ItemImageUrl = models.CharField(max_length=250,blank=True)
	LotNo = models.CharField(max_length=100,blank=True,null=True)
	SerialNo = models.CharField(max_length=100,blank=True,null=True)
	Custom1 = models.CharField(max_length=250,blank=True,null=True)
	Custom2 = models.CharField(max_length=250,blank=True,null=True)
	Custom3 = models.CharField(max_length=250,blank=True,null=True)
	Custom4 = models.CharField(max_length=250,blank=True,null=True)
	Custom5 = models.CharField(max_length=250,blank=True,null=True)
	Custom6 = models.CharField(max_length=250,blank=True,null=True)
	Custom7 = models.CharField(max_length=250,blank=True,null=True)
	Custom8 = models.CharField(max_length=250,blank=True,null=True)
	Custom9 = models.CharField(max_length=250,blank=True,null=True)
	Custom10 = models.CharField(max_length=250,blank=True,null=True)

	def __str__(self):
		return self.JobTaskId

	def __repr__(self):
		return self.JobTaskId

	def get_data(self):
		return hlp_get_data(self)


class PutawayTaskResults(models.Model):
	JobId = models.ForeignKey(PutawayJobs, on_delete=models.CASCADE)
	JobTaskId = models.CharField(max_length=50)
	InnerLicensePlate = models.CharField(max_length=50,blank=True,null=True)
	OrderId = models.CharField(max_length=50,blank=True,null=True)
	OrderLineId = models.CharField(max_length=50,blank=True,null=True)
	OrderTaskId = models.CharField(max_length=50,blank=True,null=True)
	OrderType = models.CharField(max_length=50,blank=True,null=True)
	CustOwner = models.CharField(max_length=50,null=True)
	SiteId = models.CharField(max_length=50,null=True)
	TaskStatus = models.CharField(max_length=50,blank=True,null=True)
	TaskType = models.CharField(max_length=50)
	TaskLocation = models.CharField(max_length=50)
	TaskQty = models.IntegerField()
	ExecQty = models.IntegerField(blank=True,null=True)
	ExecUser = models.CharField(max_length=50,blank=True,null=True)
	ExecDate = models.CharField(max_length=25,blank=True,null=True)
	ExecRobot = models.CharField(max_length=50,blank=True,null=True)
	ItemNo = models.CharField(max_length=50)
	LotNo = models.CharField(max_length=100,blank=True,null=True)
	SerialNo = models.CharField(max_length=100,blank=True,null=True)
	ExceptionCode = models.CharField(max_length=50,blank=True,null=True)
	ExceptionReason = models.CharField(max_length=50,blank=True,null=True)
	Custom1 = models.CharField(max_length=250,blank=True,null=True)
	Custom2 = models.CharField(max_length=250,blank=True,null=True)
	Custom3 = models.CharField(max_length=250,blank=True,null=True)
	Custom4 = models.CharField(max_length=250,blank=True,null=True)
	Custom5 = models.CharField(max_length=250,blank=True,null=True)
	Custom6 = models.CharField(max_length=250,blank=True,null=True)
	Custom7 = models.CharField(max_length=250,blank=True,null=True)
	Custom8 = models.CharField(max_length=250,blank=True,null=True)
	Custom9 = models.CharField(max_length=250,blank=True,null=True)
	Custom10 = models.CharField(max_length=250,blank=True,null=True)
	timestamp = models.DateTimeField(auto_now=True)

	@classmethod
	def get_last_task(cls,JobId,JobTaskId):
		''' get the data for the last task sent '''
		tasks = cls.objects.filter(JobId_id=JobId,JobTaskId=JobTaskId).order_by('-timestamp')
		return tasks[0]

	def __str__(self):
		return ('{}: {}'.format(self.id, self.JobTaskId))

	def __repr__(self):
		return ('{}: {}'.format(self.id, self.JobTaskId))

	def get_data(self):
		return hlp_get_data(self)


class OrderJobEvents(models.Model):
	JobId = models.ForeignKey(OrderJobs, on_delete=models.CASCADE)
	EventType = models.CharField(max_length=50)
	JobDate = models.CharField(max_length=25)
	EventInfo = models.CharField(max_length=250)
	timestamp = models.DateTimeField(auto_now=True)

	@classmethod
	def get_last_event(cls,JobId):
		last_event = cls.objects.filter(JobId=JobId).order_by('-timestamp')
		return last_event[0]

	def __str__(self):
		return('{}: {}'.format(self.JobId, self.EventType))

	def __repr__(self):
		return('{}: {}'.format(self.JobId, self.EventType))

	def get_data(self):
		return hlp_get_data(self)
	

class PutawayJobEvents(models.Model):
	JobId = models.ForeignKey(PutawayJobs, on_delete=models.CASCADE)
	EventType = models.CharField(max_length=50)
	JobDate = models.CharField(max_length=25)
	EventInfo = models.CharField(max_length=250)
	timestamp = models.DateTimeField(auto_now=True)

	def __str__(self):
		return('{}: {}'.format(self.JobId, self.EventType))

	def __repr__(self):
		return('{}: {}'.format(self.JobId, self.EventType))

	def get_data(self):
		return hlp_get_data(self)

	def get_last_event(JobId):
		return


class OrderSerialNumbers(models.Model):
	JobId = models.ForeignKey(OrderJobs, on_delete=models.CASCADE)
	JobTaskId = models.ForeignKey(OrderTaskResults, on_delete=models.CASCADE)
	SerialNo = models.CharField(max_length=100,null=False)


class ExternalUsers(models.Model):
	username_validator = UnicodeUsernameValidator()
	password = models.CharField( ("password"), max_length=128)
	username = models.CharField(
		("username"),
		max_length=150,
		unique=True,
		help_text= (
			"Required. 150 characters or fewer. Letters, digits and @/./+/-/_ only."
		),
		validators=[username_validator],
		error_messages={
			"unique": ("A user with that username already exists."),
		},
	)
	csrf_token = models.CharField(max_length=32,null=False)
	sessionid = models.CharField(max_length=32,null=False)
	system = models.CharField(max_length=3,null=False)
	created_by= models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        null=True
    )


class ExternalSystems(models.Model):
	system = models.CharField(max_length=3,null=False)
	url    = models.CharField(max_length=255,null=False)

	def __str__(self):
		return('{}: {}'.format(self.system, self.url))

	def __repr__(self):
		return('{}: {}'.format(self.system, self.url))