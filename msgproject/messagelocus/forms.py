from django import forms
from .models import OrderTaskData

class TaskDataForm(forms.ModelForm):
	class Meta:
		model = OrderTaskData
		fields = "__all__"
		
	def __init__(self, *args, **kwargs):
		super().__init__(*args, **kwargs)
		#self.fields["JobId"].disabled = True
		#self.fields["JobTaskId"].disabled = True
		# Or to set READONLY
		self.fields["JobId"].widget.attrs["readonly"] = True
		self.fields["JobTaskId"].widget.attrs["readonly"] = True
		self.fields["TaskType"].widget.attrs["readonly"] = True
