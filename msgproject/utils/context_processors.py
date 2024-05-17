# utils/context_processors.py

from core.models import ExternalServices

def system_context(request):
	if request.user.is_authenticated:
		services = []
		systems = []
		for service in ExternalServices.objects.all():
			for system in service.systems.all():
				systems.append({'system':system, 'users':[{'username':user.username, 'active':user.active} for user in system.users.all()]})
			service = {'app': service.service, 
					   'service':service.name, 
					   'systems':systems}
			services.append(service)
	else: 
		services = []

	return {'services': services}

def user_context(request):
	if request.user.is_authenticated:
		try:
			index = request.path[1:].index('/')+1
			service = ExternalServices.objects.filter(service=request.path[1:index]).first()
			system = service.systems.filter(system=request.path[index+1:index+request.path[index+1:].index('/')+1]).first()
			users = system.users.filter(created_by=request.user,sessionid=request.COOKIES['sessionid']).all()
		except (ValueError, LookupError, AttributeError):
			users = []
			service = None
			system = None
	else:
		users = []
		service = None
		system = None

	return {'system_users': {'service': service,
							  'system': system,
							   'users': [{'username':user.username,'active':user.active} for user in users]}}