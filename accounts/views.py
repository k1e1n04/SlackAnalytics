from django.shortcuts import render
from django.contrib.auth.forms import UserCreationForm
from django.urls import reverse_lazy
from django .views import generic
from .models import User

# Create your views here.
class SignUpView(generic.CreateView):
    form_class = UserCreationForm
    success_url = reverse_lazy('analytics:base_dashboard')
    template_name = 'accounts/signup.html'

class UserList(generic.ListView):
    template_name = "accounts/user_list.html"
    model = User
