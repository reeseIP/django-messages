from django import forms
from .models import OrderTaskResultData, PutawayTaskResultData

class OrderTaskDataForm(forms.ModelForm):
	class Meta:
		model = OrderTaskResultData
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

class PutawayTaskDataForm(forms.ModelForm):
	class Meta:
		model = PutawayTaskResultData
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