--- Initial Setup ---

requires python 3.9.1 interpreter
	- download python 3.9.1 @ https://www.python.org/downloads/

*** instructions for deployment from command line ***
create virtual environmen in target directory
	- python -m venv env

activate virtural environment
	- env\scripts\activate

clone or copy repository from github into target directory
	- git clone https://github.com/reeseIP/django-messages

navigate to directory containing requirements.txt and install
	- pip install -r requirements.txt 
	- warning! double check this file contents match github

create super user and database migrations
	- django-messages\msgproject
		- python manage.py createsuperuser
		- python manage.py migrate

generate a new secret key
	- python manage.py shell
		- from django.core.management.utils import get_random_secret_key
		- print(get_random_secret_key())

.env file
	- DEBUG = False
	- SECRET_KEY = newly generated key

start the server
	- python manage.py runserver

create services with admin console
	- http://domain.name:8000/admin/core/externalservices/
	- appname : description

create target systems with admin console
	- http://domain.name:8000/admin/core/externalsystems/


*** instructions for deployment on windows iis ***
install git
$ git config --global user.name "User"
$ git config --global user.email "user@user.com"

create folder for app on root

create the virtual environment
	- python -m venv env

clone repository into folder
	- https://github.com/reeseIP/django-messages

activate virtual env

navigate to folder with requirements
	- pip install -r requirements.txt

python manage.py makemigrations
python manage.py migrate
python manage.py collectstatic
python manage.py createsuperuser

manage settings.py
	- ALLOWED_HOSTS

generate a new secret key
	- python manage.py shell
		- from django.core.management.utils import get_random_secret_key
		- print(get_random_secret_key())

.env file
	- DEBUG = False
	- SECRET_KEY = newly generated key

ensure CGI feature is installed on IIS

WINDOWS IIS Server Manager
Configure FastCGI settings on IIS server
	- add application
		* Full Path: G:\message-app\env\Scripts\python.exe
		* Arguments: G:\message-app\env\Lib\site-packages\wfastcgi.py
		* Environment Variables: PYTHONPATH: G:\message-app\msgproject
					 DJANGO_SETTINGS_MODULE: msgproject.settings
				 	 WSGI_HANDLER: django.core.wsgi.get_wsgi_application()

Add website:
	- Physical Path:G:\message-app\msgproject
	- Handler Mappings: Add module mapping FastCgiModule
		* G:\message-app\env\Scripts\python.exe|G:\message-app\env\Lib\site-packages\wfastcgi.py
		* Click the “Request Restrictions” button and uncheck the “Invoke handler only if the request is mapped to the” checkbox
		* When prompted “Do you want to create a FastCGI application for this executable?” click “No” since we created the application earlier.

Firewall settings
 -ensure the port we use is open

Set the site bindings
convert the static folder to application
	- Physical Path: G:\message-app\msgproject\static
remove the django handler for static application

start the server
	- python manage.py runserver

create services with admin console
	- http://domain.name:8000/admin/core/externalservices/
	- appname : description

create target systems with admin console
	- http://domain.name:8000/admin/core/externalsystems/