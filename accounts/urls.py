from django.urls import path
from . import views
from django.contrib.auth import views as auth_views

app_name = 'accounts'

urlpatterns = [
    path('signup/',views.SignUpView.as_view(),name='signup'),
    path('index/',views.UserList.as_view(),name='index'),
    path('delete/<int:pk>/',views.UserDeleteView.as_view(),name='delete'), 
    path('update/<int:pk>/',views.UserUpdateView.as_view(),name='update'), 
    path('password_change_form/', auth_views.PasswordChangeView.as_view(template_name='registration/password_change_form.html'), name='password_change_form'),
    path('password_change_done/', auth_views.PasswordChangeDoneView.as_view(template_name='registration/password_change_done.html'), name='password_change_done'), 
]