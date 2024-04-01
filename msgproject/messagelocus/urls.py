# urls.py
from django.urls import path 
from . import views 

urlpatterns = [
	path("", views.index, name='index'),
	path("<system>/", views.active, name='active'),
	path("<system>/active/", views.active, name='active'),
	path("<system>/closed/", views.closed, name='closed'),
	path("<system>/inbound/", views.inbound, name='inbound'),
	path("<system>/check_job_exists/", views.check_job_exists, name='check_job_exists'),
	path("<system>/get_target_user/", views.get_target_user, name='get_target_user'),
	path("<system>/set_target_user/", views.set_target_user, name='set_target_user'),
	path("<system>/delete_target_user/", views.delete_target_user, name='delete_target_user'),
	path("<system>/putawayjobrequest/", views.putawayjobrequest, name='putawayjobrequest'),
	path("<system>/<JobId>/", views.jobview, name='jobview'),
	path("<system>/<JobId>/accept/", views.sendaccept, name='sendaccept'),
	path("<system>/<JobId>/reject/", views.sendreject, name='sendreject'),
	path("<system>/<JobId>/induct/", views.sendinduct, name='sendinduct'),
	path("<system>/<JobId>/complete/", views.sendcomplete, name='sendcomplete'),
	path("<system>/<JobId>/cancelcomplete/", views.sendcancelcomplete, name='sendcancelcomplete'),
	path("<system>/<JobId>/cancelreject/", views.sendcancelreject, name='sendcancelreject'),
	path("<system>/<JobId>/updatecomplete/", views.sendupdatecomplete, name='sendupdatecomplete'),
	path("<system>/<JobId>/updatereject/", views.sendupdatereject, name='sendupdatereject'),
	path("<system>/<JobId>/task/", views.sendtask, name='sendtask'),
	path("<system>/<JobId>/print/", views.sendprint, name='sendprint'),
	path("<system>/<JobId>/close_job/", views.close_job, name='close_job'),
	path("<system>/<JobId>/get_capture_field_data/", views.get_capture_field_data, name='get_capture_field_data'),
	path("<system>/<JobId>/validate_serial_number/", views.validate_serial_number, name='validate_serial_number'),
]