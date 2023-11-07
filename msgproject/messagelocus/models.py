from django.db import models

# Create your models here.

class OrderJobData(models.Model):
	EventType = models.CharField(max_length=50)
	JobId = models.CharField(max_length=50)
	JobDate = models.CharField(max_length=25)
	JobPriority = models.IntegerField(blank=True,null=True)
	JobPriorityGroup = models.CharField(max_length=50,blank=True)
	RequestId = models.CharField(max_length=50)
	ToteId = models.CharField(max_length=50)
	SingleUnit = models.BooleanField(blank=True)
	NextWorkArea = models.CharField(max_length=50, blank=True)

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
			   })


class OrderTaskData(models.Model):
	JobId = models.ForeignKey(OrderJobData, on_delete=models.CASCADE)
	JobTaskId = models.CharField(max_length=50)
	EventAction = models.CharField(max_length=50,blank=True)
	OrderId = models.CharField(max_length=50,blank=True)
	OrderLineId = models.CharField(max_length=50,blank=True)
	OrderTaskId = models.CharField(max_length=50,blank=True)
	OrderType = models.CharField(max_length=50,blank=True)
	CustOwner = models.CharField(max_length=50)
	SiteId = models.CharField(max_length=50)
	TaskType = models.CharField(max_length=50)
	TaskSequence = models.IntegerField(blank=True,null=True)
	TaskSubSequence = models.IntegerField(blank=True,null=True)
	TaskTravelPriority = models.IntegerField(blank=True,null=True)
	TaskLocation = models.CharField(max_length=50)
	TaskZone = models.CharField(max_length=50,blank=True)
	TaskWorkArea = models.CharField(max_length=50,blank=True)
	TaskQty = models.IntegerField()
	ItemNo = models.CharField(max_length=50)
	ItemUPC = models.CharField(max_length=50,blank=True)
	ItemDesc = models.CharField(max_length=50)
	ItemStyle = models.CharField(max_length=50,blank=True)
	ItemColor = models.CharField(max_length=50,blank=True)
	ItemSize = models.CharField(max_length=50,blank=True)
	ItemLength = models.DecimalField(max_digits=5,decimal_places=2,blank=True,null=True)
	ItemWidth = models.DecimalField(max_digits=5,decimal_places=2,blank=True,null=True)
	ItemHeight = models.DecimalField(max_digits=5,decimal_places=2,blank=True,null=True)
	ItemWeight = models.DecimalField(max_digits=5,decimal_places=2,blank=True,null=True)
	ItemImageUrl = models.CharField(max_length=250,blank=True)
	Custom1 = models.CharField(max_length=250,blank=True)
	Custom2 = models.CharField(max_length=250,blank=True)
	Custom3 = models.CharField(max_length=250,blank=True)
	Custom4 = models.CharField(max_length=250,blank=True)
	Custom5 = models.CharField(max_length=250,blank=True)
	Custom6 = models.CharField(max_length=250,blank=True)
	Custom7 = models.CharField(max_length=250,blank=True)
	Custom8 = models.CharField(max_length=250,blank=True)
	Custom9 = models.CharField(max_length=250,blank=True)
	Custom10 = models.CharField(max_length=250,blank=True)
	LotNo = models.CharField(max_length=250,blank=True)
	SerialNo = models.CharField(max_length=250,blank=True)
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


class PutawayJobData(models.Model):
	EventType = models.CharField(max_length=50)
	EventInfo = models.CharField(max_length=50)
	LicensePlate = models.CharField(max_length=50)
	RequestId = models.CharField(max_length=50)
	JobId = models.CharField(max_length=50)
	JobDate = models.CharField(max_length=25)
	JobPriority = models.IntegerField()


class PutawayTaskData(models.Model):
	JobId = models.ForeignKey(PutawayJobData, on_delete=models.CASCADE)
	JobTaskId = models.CharField(max_length=50)
	EventAction = models.CharField(max_length=50,blank=True)
	InnerLicensePlate = models.CharField(max_length=50)
	OrderId = models.CharField(max_length=50)
	OrderLineId = models.CharField(max_length=50)
	OrderTaskId = models.CharField(max_length=50)
	OrderType = models.CharField(max_length=50)
	CustOwner = models.CharField(max_length=50)
	SiteId = models.CharField(max_length=50)
	TaskType = models.CharField(max_length=50)
	TaskTravelPriority = models.IntegerField()
	TaskLocation = models.CharField(max_length=50)
	TaskZone = models.CharField(max_length=50)
	TaskWorkArea = models.CharField(max_length=50)
	TaskQty = models.IntegerField()
	ItemNo = models.CharField(max_length=50)
	ItemUPC = models.CharField(max_length=50)
	ItemDesc = models.CharField(max_length=50)
	ItemStyle = models.CharField(max_length=50)
	ItemColor = models.CharField(max_length=50)
	ItemSize = models.CharField(max_length=50)
	ItemLength = models.DecimalField(max_digits=5, decimal_places=2)
	ItemWidth = models.DecimalField(max_digits=5, decimal_places=2)
	ItemHeight = models.DecimalField(max_digits=5, decimal_places=2)
	ItemWeight = models.DecimalField(max_digits=5, decimal_places=2)
	ItemImageUrl = models.CharField(max_length=250)
	LotNo = models.CharField(max_length=100)
	SerialNo = models.CharField(max_length=100)
	Custom1 = models.CharField(max_length=250)
	Custom2 = models.CharField(max_length=250)
	Custom3 = models.CharField(max_length=250)
	Custom4 = models.CharField(max_length=250)
	Custom5 = models.CharField(max_length=250)
	Custom6 = models.CharField(max_length=250)
	Custom7 = models.CharField(max_length=250)
	Custom8 = models.CharField(max_length=250)
	Custom9 = models.CharField(max_length=250)
	Custom10 = models.CharField(max_length=250)


class JobStatus(models.Model):
	JobId = models.CharField(max_length=50)
	status = models.CharField(max_length=250)