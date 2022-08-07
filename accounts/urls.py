from django.urls import path
from . import views

app_name = 'accounts'

urlpatterns = [
    path('signup/',views.SignUpView.as_view(),name='signup'),
    path('index/',views.UserList.as_view(),name='index'),
    path('delete/<int:pk>/',views.UserDeleteView.as_view(),name='delete'), 
]