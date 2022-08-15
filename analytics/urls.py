from django.urls import path
from . import views

app_name = 'analytics'

urlpatterns = [
    path('',views.base_dashboard.as_view(),name='base_dashboard'),
    #ダッシュボード
    path('basedashboard/',views.base_dashboard.as_view(),name='base_dashboard'),
    path('channeldashboard/',views.channel_dashboard.as_view(),name='channel_dashboard'),
    path('employeedashboard/',views.employee_dashboard.as_view(),name='employee_dashboard'),
    path('employeedashboard/<int:pk>',views.employee_detail_dashboard.as_view(),name='employee_detail_dashboard'),
    #拠点関連
    path('base/index/',views.BaseListView.as_view(),name='base_index'),
    path('base/create/', views.BaseCreateView.as_view(), name='base_create'),
    #部署関連
    path('department/index/',views.DepartmentListView.as_view(),name='department_index'),
    path('department/create/', views.DepartmentCreateView.as_view(), name='department_create'),
    path('department/update/<int:pk>/', views.DepartmentUpdateView.as_view(), name='department_update'),
    path('department/delete/<int:pk>/', views.DepartmentDeleteView.as_view(), name='department_delete'),
    #メンバー関連
    path('employee/index/',views.EmployeeListView.as_view(),name='employee_index'),
    path('employee/create/', views.EmployeeCreateView.as_view(), name='employee_create'),
    path('employee/update/<int:pk>/', views.EmployeeUpdateView.as_view(), name='employee_update'),
    path('employee/delete/<int:pk>/', views.EmployeeDeleteView.as_view(), name='employee_delete'),
    #チャンネル関連
    path('channel/index/',views.ChannelListView.as_view(),name='channel_index'),
    path('channel/create/', views.ChannelCreateView.as_view(), name='channel_create'),
    path('channel/update/<int:pk>/', views.ChannelUpdateView.as_view(), name='channel_update'),
    path('channel/delete/<int:pk>/', views.ChannelDeleteView.as_view(), name='channel_delete')
]