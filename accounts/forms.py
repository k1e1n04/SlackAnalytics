from django import forms
from django.contrib.auth.forms import (
    UserCreationForm
)
from django.contrib.auth import get_user_model

User = get_user_model()

class UserCreateForm(UserCreationForm):
    class Meta:
        model = User
        fields = ('username','last_name','first_name','base')

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field in self.fields.values():
            field.widget.attrs['class'] = 'form-control'

class UserUpdateForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ('username','last_name','first_name')

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field in self.fields.values():
            field.widget.attrs['class'] = 'form-control'