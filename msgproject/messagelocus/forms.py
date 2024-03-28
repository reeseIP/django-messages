# forms.py
from django import forms
from .models import OrderTaskResults, PutawayTaskResults

class OrderTasksForm(forms.ModelForm):
	class Meta:
		model = OrderTaskResults
		fields = "__all__"
		exclude = ['JobId']
		
	def __init__(self, *args, **kwargs):
		super().__init__(*args, **kwargs)
		# set fields to READONLY
		self.fields["JobTaskId"].widget.attrs["readonly"] = True
		self.fields["TaskType"].widget.attrs["readonly"] = True

class PutawayTasksForm(forms.ModelForm):
	class Meta:
		model = PutawayTaskResults
		fields = "__all__"
		exclude = ['JobId']
		
	def __init__(self, *args, **kwargs):
		super().__init__(*args, **kwargs)
		self.fields["JobTaskId"].widget.attrs["readonly"] = True
		self.fields["TaskType"].widget.attrs["readonly"] = True