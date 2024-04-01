from django.db import models

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



#class ExternalServices(models.Model, ModelHelp):
#	service = models.CharField(max_length=50,null=False)
#	name    = models.CharField(max_length=250)
#	path 	= models.CharField(max_length=52)
#
#	def __str__(self):
#		return('{}: {}'.format(self.service, self.name))
#
#	def __repr__(self):
#		return('{}: {}'.format(self.service, self.name))