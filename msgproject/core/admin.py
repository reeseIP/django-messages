from django.contrib import admin
from .models import ExternalServices, ExternalSystems, ExternalUsers

# register your models here
admin.site.register(ExternalServices)
admin.site.register(ExternalSystems)
admin.site.register(ExternalUsers)

