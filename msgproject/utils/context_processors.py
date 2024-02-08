# utils/context_processors.py

from messagelocus.models import ExternalSystems, ExternalUsers

def system_context(request):
	systems = []
	system_query = ExternalSystems.objects.all()
	for system in system_query:
		systems.append(system.system)
	return {'systems': systems}

def user_context(request):
	if request.user.is_authenticated:
		user_query = ExternalUsers.objects.filter(created_by=request.user)
		return {'active_users':user_query}
	else:
		return{'active_users':''}