from django.contrib import admin
from .models import OrderJobData, OrderTaskData, PutawayJobData, PutawayTaskData, PutawayTaskResultData, OrderJobEvents, PutawayJobEvents, ExternalUsers, ExternalSystems


# Register your models here.
admin.site.register(OrderJobData)
admin.site.register(OrderTaskData)
admin.site.register(PutawayJobData)
admin.site.register(PutawayTaskData)
admin.site.register(PutawayTaskResultData)
admin.site.register(OrderJobEvents)
admin.site.register(PutawayJobEvents)
admin.site.register(ExternalUsers)
admin.site.register(ExternalSystems)