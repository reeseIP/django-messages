# admin.py
from django.contrib import admin
from .models import ( ExternalSystems, ExternalUsers, 
					  OrderJobs, OrderJobResults, OrderTasks, OrderTaskResults, OrderSerialNumbers, OrderJobEvents,
					  PutawayJobs, PutawayJobResults, PutawayTasks, PutawayTaskResults, PutawayJobEvents)


# register models
admin.site.register(ExternalSystems)
admin.site.register(ExternalUsers)
admin.site.register(OrderJobs)
admin.site.register(OrderJobResults)
admin.site.register(OrderTasks)
admin.site.register(OrderTaskResults)
admin.site.register(OrderSerialNumbers)
admin.site.register(OrderJobEvents)
admin.site.register(PutawayJobs)
admin.site.register(PutawayJobResults)
admin.site.register(PutawayTasks)
admin.site.register(PutawayTaskResults)
admin.site.register(PutawayJobEvents)


