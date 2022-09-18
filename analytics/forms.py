from .models import Employee
from django import forms


class EmployeeForm(forms.ModelForm):
    class Meta:
        model = Employee
        fields = ('name', 'base', 'department','slack_id')
    
    field_order= ('name', 'base', 'department','slack_id')

