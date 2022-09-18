from audioop import reverse
from django.shortcuts import render
from django.contrib.auth.forms import PasswordChangeForm
from django.urls import reverse_lazy
from django .views import generic
from .models import User
from django.contrib.auth.mixins import LoginRequiredMixin,UserPassesTestMixin
from django.contrib.auth.views import PasswordChangeView,PasswordChangeDoneView,PasswordContextMixin
from .forms import (
    UserCreateForm,
    UserUpdateForm
)

class OnlyYouMixin(UserPassesTestMixin):
    raise_exception = False

    def test_func(self):
        user = self.request.user
        return user.pk == self.kwargs['pk'] or user.is_staff


# Create your views here.
class SignUpView(LoginRequiredMixin,generic.CreateView):
    form_class = UserCreateForm
    success_url = reverse_lazy('analytics:base_dashboard')
    template_name = 'accounts/signup.html'

class UserList(LoginRequiredMixin,generic.ListView):
    template_name = "accounts/user_list.html"
    def get_queryset(self):
        try:
            query= self.request.GET.get('query')
        except:
            query = None
        users = User.objects.user_search(query=query)
        return users

class UserDeleteView(OnlyYouMixin,generic.DeleteView):
    model = User
    template_name = "accounts/user_delete.html"
    success_url = reverse_lazy('accounts:index')

class UserUpdateView(OnlyYouMixin,generic.UpdateView):
    model = User
    form_class = UserUpdateForm
    success_url = reverse_lazy('analytics:base_dashboard')
    template_name = 'accounts/update.html'

class PasswordChangeView(OnlyYouMixin,PasswordContextMixin, generic.FormView):
    form_class = PasswordChangeForm
    success_url = reverse_lazy('password_change_done')
    template_name = 'registration/password_change_form.html'
    title = 'Password change'

class PasswordChangeDoneView(PasswordContextMixin, generic.TemplateView):
    template_name = 'registration/password_change_done.html'
    title = 'Password change successful'