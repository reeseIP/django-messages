# forms.py
from django import forms
from .models import OrderTaskResults, PutawayTaskResults

class OrderTasksForm(forms.ModelForm):
	class Meta:
		model = OrderTaskResults
		fields = OrderTaskResults.get_fields()
		#exclude = ['Job']
		
	def __init__(self, *args, **kwargs):
		super().__init__(*args, **kwargs)
		# set fields to READONLY
		self.fields["JobTaskId"].widget.attrs["readonly"] = True
		self.fields["TaskType"].widget.attrs["readonly"] = True
		

class PutawayTasksForm(forms.ModelForm):
	class Meta:
		model = PutawayTaskResults
		fields = PutawayTaskResults.get_fields()
		#exclude = ['Job']
		
	def __init__(self, *args, **kwargs):
		super().__init__(*args, **kwargs)
		self.fields["JobTaskId"].widget.attrs["readonly"] = True
		self.fields["TaskType"].widget.attrs["readonly"] = True