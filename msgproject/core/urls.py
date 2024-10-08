from django.urls import path 
from . import views 

urlpatterns = [
	path("", views.index, name='index'),
	path("login/", views.login_user, name='login_user'),
	path("logout/", views.logout_user, name='logout_user'),
	path("register/", views.register_user, name='register_user'),
	path("search/<search>/", views.search, name='search'),
	path("set_target_user/<service>/<system>/<username>/", views.set_target_user, name='set_target_user'),
	path("delete_target_user/<service>/<system>/<username>/", views.delete_target_user, name='delete_target_user'),
]