from django.urls import path 
from . import views 

urlpatterns = [
	path("", views.index, name='index'),
	path("login/", views.login_user, name='login_user'),
	path("logout/", views.logout_user, name='logout_user'),
	path("inbound/", views.inbound, name='inbound'),
	path("<JobId>/", views.jobview, name='jobview'),
	path("<JobId>/accept/", views.sendaccept, name='sendaccept'),
	path("<JobId>/reject/", views.sendreject, name='sendreject'),
	path("<JobId>/toteinduct/", views.sendtoteinduct, name='sendtoteinduct'),
	path("<JobId>/pickcomplete/", views.sendpickcomplete, name='sendpickcomplete'),
	path("<JobId>/cancelcomplete/", views.sendcancelcomplete, name='sendcancelcomplete'),
	path("<JobId>/cancelreject/", views.sendcancelreject, name='sendcancelreject'),
	path("<JobId>/updatecomplete/", views.sendupdatecomplete, name='sendupdatecomplete'),
	path("<JobId>/updatereject/", views.sendupdatereject, name='sendupdatereject'),
	path("<JobId>/task/", views.sendtask, name='sendtask'),
]