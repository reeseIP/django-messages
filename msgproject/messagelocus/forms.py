from django import forms
from .models import OrderTaskResults, PutawayTaskResults

class OrderTasksForm(forms.ModelForm):
	class Meta:
		model = OrderTaskResults
		fields = "__all__"
		exclude = ['JobId']
		
	def __init__(self, *args, **kwargs):
		super().__init__(*args, **kwargs)
		#self.fields["JobId"].disabled = True
		#self.fields["JobTaskId"].disabled = True
		# Or to set READONLY
		#self.fields["JobId"].widget.attrs["readonly"] = True
		self.fields["JobTaskId"].widget.attrs["readonly"] = True
		self.fields["TaskType"].widget.attrs["readonly"] = True

class PutawayTasksForm(forms.ModelForm):
	class Meta:
		model = PutawayTaskResults
		fields = "__all__"
		exclude = ['JobId']
		
	def __init__(self, *args, **kwargs):
		super().__init__(*args, **kwargs)
		#self.fields["JobId"].disabled = True
		#self.fields["JobTaskId"].disabled = True
		# Or to set READONLY
		#self.fields["JobId"].widget.attrs["readonly"] = True
		self.fields["JobTaskId"].widget.attrs["readonly"] = True
		self.fields["TaskType"].widget.attrs["readonly"] = True