# utils/context_processors.py

from django.apps import apps

def system_context(request):
	if request.user.is_authenticated:
		app_configs = apps.get_app_configs()
		services = []
		for app in app_configs:
			try:
				if app.service:
					service = {'app': app.name, 'service':app.display_name, 'systems':[system for system in app.get_model('ExternalSystems').objects.all()]}
					services.append(service)
					service = {'service':'Add service', 'systems':[system for system in app.get_model('ExternalSystems').objects.all()]}
					services.append(service)
			except (AttributeError, LookupError):
				pass
	else: 
		services = []
	return{'services':services}

def user_context(request):
	if request.user.is_authenticated:
		try:
			index = request.path[1:].index('/')+1
			service = request.path[1:index]
			system = request.path[index+1:index+request.path[index+1:].index('/')+1]
			app_config = apps.get_app_config(service)
			users = app_config.get_model('ExternalUsers').objects.filter(created_by=request.user,system=system,sessionid=request.COOKIES['sessionid'])
		except (ValueError, LookupError):
			users = []
	else:
		users = []
	return{'active_users': [user.username for user in users]}