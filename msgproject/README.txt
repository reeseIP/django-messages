--- Initial Setup ---

requires python 3.9.1 interpreter and git

download python 3.9.1 @ https://www.python.org/downloads/

*** instructions for deployment from command line ***
create virtual environmen in target directory
	- python -m venv env

activate virtural environment
	- env\scripts\activate

clone repository from github
	git clone https://github.com/reeseIP/django-messages

navigate to directory containing requirements.txt and install
	- pip install -r requirements.txt 
	- warning! double check this file contents match github

create super user and database migrations
	- django-messages\msgproject
		- python manage.py createsuperuser
		- python manage.py migrate

settings.py
	- DEBUG = False
	- ALLOWED_HOSTS = [ 'site domain here' ]

start the server
	- python manage.py runserver

create target system entries with admin console
	- http://domain.name:8000/admin/messagelocus/externalsystems/

