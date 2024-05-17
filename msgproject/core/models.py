from django.db import models
from django.conf import settings
from django.contrib.auth.validators import UnicodeUsernameValidator

# Create your models here.

class ModelHelp():

	def get_data(self, excluded_fields=False):
		if not excluded_fields:
			exclude_fields = self._meta.exclude_fields
		else:
			exclude_fields = []
		data = {}
		fields = self._meta.get_fields()
		for field in fields:
			if 'Field' in type(field).__name__:
				valid = True
				for exfield in exclude_fields:
					if exfield in field.name:
						valid = False
				if valid:
					attr = getattr(self,field.name)
					if attr == None:
						attr = ""
					data[field.name] = attr
		return(data)

	@classmethod
	def get_fields(cls, excluded_fields=False):
		if not excluded_fields:
			exclude_fields = cls._meta.exclude_fields
		else:
			exclude_fields = []
		data = {}
		fields = cls._meta.get_fields()
		for field in fields:
			if 'Field' in type(field).__name__:
				valid = True
				for exfield in exclude_fields:
					if exfield in field.name:
						valid = False
				if valid:
					data[field.name] = ""
		return(data)


class ExternalServices(models.Model, ModelHelp):
	service = models.CharField(max_length=50,null=False, primary_key=True) # app name
	name    = models.CharField(max_length=250)

	def __str__(self):
		return('{}: {}'.format(self.service, self.name))

	def __repr__(self):
		return('{}: {}'.format(self.service, self.name))


class ExternalSystems(models.Model, ModelHelp):
	system  = models.CharField(max_length=3,null=False)
	name 	= models.CharField(max_length=100)
	url     = models.CharField(max_length=250,null=False)
	service = models.ForeignKey(ExternalServices, on_delete=models.CASCADE, related_name='systems')

	def __str__(self):
		return('{}: {}'.format(self.system, self.url))

	def __repr__(self):
		return('{}: {}'.format(self.system, self.url))


class ExternalUsers(models.Model, ModelHelp):
	username_validator = UnicodeUsernameValidator()
	username   = models.CharField(
					("username"),
					max_length=150,
					help_text= (
						"Required. 150 characters or fewer. Letters, digits and @/./+/-/_ only."
					),
					validators=[username_validator],
				 )
	password   = models.CharField( ("password"), max_length=128)
	sessionid  = models.CharField(max_length=32,null=False)
	system 	   = models.ForeignKey(ExternalSystems, on_delete=models.CASCADE, related_name='users')
	created_by = models.ForeignKey(
			        settings.AUTH_USER_MODEL,
			        on_delete=models.CASCADE,
			        null=True
    			 )
	active     = models.BooleanField(default=False)

	def __str__(self):
		return('{}: {}'.format(self.system_id, self.username))

	def __repr__(self):
		return('{}: {}'.format(self.system_id, self.username))
