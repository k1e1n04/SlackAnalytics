from django.urls import path
from . import views

app_name = 'analytics'

urlpatterns = [
    path('', views.toya_analytics, name='toya_analytics')
]