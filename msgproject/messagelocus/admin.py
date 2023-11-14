from django.contrib import admin
from .models import OrderJobData, OrderTaskData, PutawayJobData, PutawayTaskData, PutawayTaskResultData, JobStatus, ExternalAuth


# Register your models here.
admin.site.register(OrderJobData)
admin.site.register(OrderTaskData)
admin.site.register(PutawayJobData)
admin.site.register(PutawayTaskData)
admin.site.register(PutawayTaskResultData)
admin.site.register(JobStatus)
admin.site.register(ExternalAuth)