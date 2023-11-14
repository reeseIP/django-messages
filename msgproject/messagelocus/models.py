from django.db import models

from django.contrib.auth.validators import UnicodeUsernameValidator

# Create your models here.

class OrderJobData(models.Model):
	EventType = models.CharField(max_length=50)
	JobId = models.CharField(max_length=50)
	JobDate = models.CharField(max_length=25)
	JobPriority = models.CharField(max_length=10,blank=True,null=True)
	JobPriorityGroup = models.CharField(max_length=50,blank=True,null=True)
	RequestId = models.CharField(max_length=50)
	ToteId = models.CharField(max_length=50)
	SingleUnit = models.BooleanField(default=False,null=True)
	NextWorkArea = models.CharField(max_length=50, blank=True, null=True)
	JobRobot = models.CharField(max_length=50, blank=True, null=True)

	def __str__(self):
		return self.JobId

	def __repr__(self):
		return self.JobId

	def get_data(self):
		return({'id': self.id,
				'EventType': self.EventType,
				'JobId': self.JobId,
				'JobDate': self.JobDate,
				'JobPriority': self.JobPriority,
				'JobPriorityGroup': self.JobPriorityGroup,
				'RequestId': self.RequestId,
				'ToteId': self.ToteId,
				'SingleUnit': self.SingleUnit,
				'NextWorkArea': self.NextWorkArea,
				'JobRobot': self.JobRobot,
			   })


class OrderTaskData(models.Model):
	JobId = models.ForeignKey(OrderJobData, on_delete=models.CASCADE)
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
		return({
			"JobId": self.JobId,
			"JobTaskId": self.JobTaskId,
			"EventAction": self.EventAction,
			"OrderId": self.OrderId,
			"OrderLineId": self.OrderLineId,
			"OrderTaskId": self.OrderTaskId,
			"OrderType": self.OrderType,
			"CustOwner": self.CustOwner,
			"SiteId": self.SiteId,
			"TaskType": self.TaskType,
			"TaskSequence": self.TaskSequence,
			"TaskSubSequence": self.TaskSubSequence,
			"TaskTravelPriority": self.TaskTravelPriority,
			"TaskLocation": self.TaskLocation,
			"TaskZone": self.TaskZone,
			"TaskWorkArea": self.TaskWorkArea,
			"TaskQty": self.TaskQty,
			"ItemNo": self.ItemNo,
			"ItemUPC": self.ItemUPC,
			"ItemDesc": self.ItemDesc,
			"ItemStyle": self.ItemStyle,
			"ItemColor": self.ItemColor,
			"ItemSize": self.ItemSize,
			"ItemLength": self.ItemLength,
			"ItemWidth": self.ItemWidth,
			"ItemHeight": self.ItemHeight,
			"ItemWeight": self.ItemWeight,
			"ItemImageUrl": self.ItemImageUrl,
			"Custom1": self.Custom1,
			"Custom2": self.Custom2,
			"Custom3": self.Custom3,
			"Custom4": self.Custom4,
			"Custom5": self.Custom5,
			"Custom6": self.Custom6,
			"Custom7": self.Custom7,
			"Custom8": self.Custom8,
			"Custom9": self.Custom9,
			"Custom10": self.Custom10,
			"LotNo": self.LotNo,
			"SerialNo": self.SerialNo,
			"CaptureLotNo": self.CaptureLotNo,
			"CaptureSerialNo": self.CaptureSerialNo,
			"CaptureSerialNoQty": self.CaptureSerialNoQty,
			})


class OrderTaskResultData(models.Model):
	JobId = models.ForeignKey(OrderJobData, on_delete=models.CASCADE)
	JobTaskId = models.CharField(max_length=50)
	OrderId = models.CharField(max_length=50,blank=True,null=True)
	OrderLineId = models.CharField(max_length=50,blank=True,null=True)
	OrderTaskId = models.CharField(max_length=50,blank=True,null=True)
	CustOwner = models.CharField(max_length=50,null=True)
	SiteId = models.CharField(max_length=50,null=True)
	TaskStatus = models.CharField(max_length=50,blank=True,null=True)
	TaskType = models.CharField(max_length=50)
	TaskLocation = models.CharField(max_length=50)
	TaskQty = models.IntegerField()
	ExecQty = models.IntegerField()
	ExecUser = models.CharField(max_length=50)
	ExecDate = models.CharField(max_length=25)
	ExecRobot = models.CharField(max_length=50)
	ItemNo = models.CharField(max_length=50)
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
	CaptureLotNo = models.BooleanField(default=False)
	CaptureSerialNo = models.BooleanField(default=False)
	CaptureSerialNoQty = models.IntegerField(default=0)
	

class PutawayJobData(models.Model):
	EventType = models.CharField(max_length=50)
	EventInfo = models.CharField(max_length=50,blank=True,null=True)
	LicensePlate = models.CharField(max_length=50)
	RequestId = models.CharField(max_length=50)
	JobId = models.CharField(max_length=50)
	JobDate = models.CharField(max_length=25)
	JobPriority = models.CharField(max_length=10,blank=True,null=True)
	JobRobot = models.CharField(max_length=50, blank=True, null=True)

	def __str__(self):
		return self.JobId

	def __repr__(self):
		return self.JobId

	def get_data(self):
		return({'id': self.id,
				'EventType': self.EventType,
				'EventInfo': self.EventType,
				'LicensePlate': self.LicensePlate,
				'RequestId': self.RequestId,
				'JobId': self.JobId,
				'JobDate': self.JobDate,
				'JobPriority': self.JobPriority,
				'JobRobot': self.JobRobot,
			   })


class PutawayTaskData(models.Model):
	JobId = models.ForeignKey(PutawayJobData, on_delete=models.CASCADE)
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
		return({
			"JobId": self.JobId,
			"JobTaskId": self.JobTaskId,
			"EventAction": self.EventAction,
			"InnerLicensePlate": self.InnerLicensePlate,
			"OrderId": self.OrderId,
			"OrderLineId": self.OrderLineId,
			"OrderTaskId": self.OrderTaskId,
			"OrderType": self.OrderType,
			"CustOwner": self.CustOwner,
			"SiteId": self.SiteId,
			"TaskType": self.TaskType,
			"TaskTravelPriority": self.TaskTravelPriority,
			"TaskLocation": self.TaskLocation,
			"TaskZone": self.TaskZone,
			"TaskWorkArea": self.TaskWorkArea,
			"TaskQty": self.TaskQty,
			"ItemNo": self.ItemNo,
			"ItemUPC": self.ItemUPC,
			"ItemDesc": self.ItemDesc,
			"ItemStyle": self.ItemStyle,
			"ItemColor": self.ItemColor,
			"ItemSize": self.ItemSize,
			"ItemLength": self.ItemLength,
			"ItemWidth": self.ItemWidth,
			"ItemHeight": self.ItemHeight,
			"ItemWeight": self.ItemWeight,
			"ItemImageUrl": self.ItemImageUrl,
			"LotNo": self.LotNo,
			"SerialNo": self.SerialNo,
			"Custom1": self.Custom1,
			"Custom2": self.Custom2,
			"Custom3": self.Custom3,
			"Custom4": self.Custom4,
			"Custom5": self.Custom5,
			"Custom6": self.Custom6,
			"Custom7": self.Custom7,
			"Custom8": self.Custom8,
			"Custom9": self.Custom9,
			"Custom10": self.Custom10,
			})


class PutawayTaskResultData(models.Model):
	JobId = models.ForeignKey(PutawayJobData, on_delete=models.CASCADE)
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

	def __str__(self):
		return self.JobTaskId

	def __repr__(self):
		return self.JobTaskId

	def get_data(self):
		return({"JobId": self.JobId,
		"JobTaskId": self.JobTaskId,
		"InnerLicensePlate": self.InnerLicensePlate,
		"OrderId": self.OrderId,
		"OrderLineId": self.OrderLineId,
		"OrderTaskId": self.OrderTaskId,
		"OrderType": self.OrderType,
		"CustOwner": self.CustOwner,
		"SiteId": self.SiteId,
		"TaskStatus": self.TaskStatus,
		"TaskType": self.TaskType,
		"TaskLocation": self.TaskLocation,
		"TaskQty": self.TaskQty,
		"ExecQty": self.ExecQty,
		"ExecUser": self.ExecUser,
		"ExecDate": self.ExecDate,
		"ExecRobot": self.ExecRobot,
		"ItemNo": self.ItemNo,
		"LotNo": self.LotNo,
		"SerialNo": self.SerialNo,
		"ExceptionCode": self.ExceptionCode,
		"ExceptionReason": self.ExceptionReason,
		"Custom1": self.Custom1,
		"Custom2": self.Custom2,
		"Custom3": self.Custom3,
		"Custom4": self.Custom4,
		"Custom5": self.Custom5,
		"Custom6": self.Custom6,
		"Custom7": self.Custom7,
		"Custom8": self.Custom8,
		"Custom9": self.Custom9,
		"Custom10": self.Custom10,
})


class JobStatus(models.Model):
	JobId = models.CharField(max_length=50)
	status = models.CharField(max_length=250)


class ExternalAuth(models.Model):
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