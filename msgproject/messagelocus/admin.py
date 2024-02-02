from django.contrib import admin
from .models import OrderJobs, OrderTasks, OrderTaskResults, PutawayJobs, PutawayTasks, PutawayTaskResults, OrderSerialNumbers, OrderJobEvents, PutawayJobEvents, ExternalUsers, ExternalSystems


# Register your models here.
admin.site.register(OrderJobs)
admin.site.register(OrderTasks)
admin.site.register(OrderTaskResults)
admin.site.register(OrderSerialNumbers)
admin.site.register(PutawayJobs)
admin.site.register(PutawayTasks)
admin.site.register(PutawayTaskResults)
admin.site.register(OrderJobEvents)
admin.site.register(PutawayJobEvents)
admin.site.register(ExternalUsers)
admin.site.register(ExternalSystems)