from .models import ExternalUsers
from django.contrib.sessions.models import Session
import threading
import time
import datetime

class BackgroundTasks(threading.Thread):
	def run(self,*args,**kwargs):
		while True:
			sessions = Session.objects.filter(expire_date__lte=datetime.datetime.now()).all()
			for session in sessions:
				ExternalUsers.objects.filter(sessionid=session.session_key).delete()
			time.sleep(3600)