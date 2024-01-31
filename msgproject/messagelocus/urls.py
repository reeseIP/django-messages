from django.urls import path 
from . import views 

urlpatterns = [
	path("", views.index, name='index'),
	path("active/", views.active, name='active'),
	path("closed/", views.closed, name='closed'),
	path("login/", views.login_user, name='login_user'),
	path("logout/", views.logout_user, name='logout_user'),
	path("inbound/", views.inbound, name='inbound'),
	path("putawayjobrequest/", views.putawayjobrequest, name='putawayjobrequest'),
	path("set_target_user/", views.set_target_user, name='set_target_user'),
	path("<JobId>/", views.jobview, name='jobview'),
	path("<JobId>/accept/", views.sendaccept, name='sendaccept'),
	path("<JobId>/reject/", views.sendreject, name='sendreject'),
	path("<JobId>/induct/", views.sendinduct, name='sendinduct'),
	path("<JobId>/complete/", views.sendcomplete, name='sendcomplete'),
	path("<JobId>/cancelcomplete/", views.sendcancelcomplete, name='sendcancelcomplete'),
	path("<JobId>/cancelreject/", views.sendcancelreject, name='sendcancelreject'),
	path("<JobId>/updatecomplete/", views.sendupdatecomplete, name='sendupdatecomplete'),
	path("<JobId>/updatereject/", views.sendupdatereject, name='sendupdatereject'),
	path("<JobId>/task/", views.sendtask, name='sendtask'),
	path("<JobId>/closejob/", views.close_job, name='close_job'),
]