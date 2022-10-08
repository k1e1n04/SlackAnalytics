from django import forms
from django.contrib.auth.forms import (
    UserCreationForm
)
from django.contrib.auth import get_user_model

User = get_user_model()

class UserCreateForm(UserCreationForm):
    """管理者ユーザー登録用のフォーム\n
    ユーザー名、名前、苗字、拠点入力用
    """
    class Meta:
        model = User
        fields = ('username','last_name','first_name','base')

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field in self.fields.values():
            field.widget.attrs['class'] = 'form-control'

class UserUpdateForm(forms.ModelForm):
    """管理者ユーザー情報更新用のフォーム\n
    ユーザー名、名前、苗字入力用
    """
    class Meta:
        model = User
        fields = ('username','last_name','first_name')

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field in self.fields.values():
            field.widget.attrs['class'] = 'form-control'