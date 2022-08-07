from django.shortcuts import render
from django.contrib.auth.forms import UserCreationForm
from django.urls import reverse_lazy
from django .views import generic
from .models import User
from django.contrib.auth.mixins import LoginRequiredMixin
from .forms import (
    UserCreateForm
)

# Create your views here.
class SignUpView(LoginRequiredMixin,generic.CreateView):
    form_class = UserCreateForm
    success_url = reverse_lazy('analytics:base_dashboard')
    template_name = 'accounts/signup.html'

class UserList(LoginRequiredMixin,generic.ListView):
    template_name = "accounts/user_list.html"
    model = User

class UserDeleteView(LoginRequiredMixin,generic.DeleteView):
    model = User
    template_name = "accounts/user_delete.html"
    success_url = reverse_lazy('accounts:index')
