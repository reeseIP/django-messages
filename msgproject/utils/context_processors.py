# utils/context_processors.py

from django.apps import apps

def system_context(request):
	if request.user.is_authenticated:
		app_configs = apps.get_app_configs()
		services = []
		systems = []
		for app in app_configs:
			try:
				if app.service:
					for system in app.get_model('ExternalSystems').objects.all():
						systems.append({'system':system, 'users':[{'username':user.username, 'active':user.active} for user in app.get_model('ExternalUsers').objects.filter(system=system.system).all()]})
					service = {'app': app.name, 
							   'service':app.display_name, 
							   'systems':systems}
					services.append(service)
	
			except (AttributeError, LookupError):
				pass
	else: 
		services = []

	return{'services': services}

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
			service = None
			system = None
	else:
		users = []

	return{'system_users': {'service': service,
							 'system': system,
							 'users': [{'username':user.username,'active':user.active} for user in users]}}