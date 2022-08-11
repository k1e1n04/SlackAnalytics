from django.urls import path
from . import views

app_name = 'analytics'

urlpatterns = [
    path('',views.base_dashboard.as_view(),name='base_dashboard'),
    #ダッシュボード
    path('basedashboard/',views.base_dashboard.as_view(),name='base_dashboard'),
    path('channeldashboard/',views.channel_dashboard.as_view(),name='channel_dashboard'),
    path('employeedashboard/',views.employee_dashboard.as_view(),name='employee_dashboard'),
    #拠点関連
    path('base/index/',views.BaseListView.as_view(),name='base_index'),
    path('base/create/', views.BaseCreateView.as_view(), name='base_create'),
    #部署関連
    path('department/index/',views.DepartmentListView.as_view(),name='department_index'),
    path('department/create/', views.DepartmentCreateView.as_view(), name='department_create'),
    #メンバー関連
    path('employee/index/',views.EmployeeListView.as_view(),name='employee_index'),
    path('employee/create/', views.EmployeeCreateView.as_view(), name='employee_create'),
    #チャンネル関連
    path('channel/index/',views.ChannelListView.as_view(),name='channel_index'),
    path('channel/create/', views.ChannelCreateView.as_view(), name='channel_create')
]