from email import message
from multiprocessing import context
from pyexpat.errors import messages
from turtle import end_poly
from django.shortcuts import render
from random import randint
from django.views import generic
import os
from .forms import EmployeeForm
from pytz import timezone, utc
from tzlocal import get_localzone
from dotenv import load_dotenv
from django.conf import settings
from .models import Base,Department,Channel,Employee,Post
from django.views import generic
from django.urls import reverse_lazy
import analytics.domain
import analytics.process.get_time

one_week_ago = analytics.process.get_time.get_diff_days_ago(7)
two_week_ago = analytics.process.get_time.get_diff_days_ago(14)

#拠点別ダッシュボード
def base_dashboard(request):
    context = {}
    dashboard = []
    bases = Base.objects.all()
    for b in bases:
        member_count = len(Employee.objects.filter(base=b))
        if member_count == 0:
            continue
        one_week_posts = Post.objects.filter(base=b,created_at__gt=one_week_ago)
        two_week_posts = Post.objects.filter(base=b,created_at__gt=two_week_ago,created_at__lte=one_week_ago)
        one_week_posts_count = len(one_week_posts)
        two_week_posts_count = len(two_week_posts)
        compare_posts_count = one_week_posts_count-two_week_posts_count
        per_posts = round(one_week_posts_count/member_count)
        compare_per_posts = round(per_posts-(two_week_posts_count/member_count))
        channel_count = len(Channel.objects.filter(base=b))
        total_posts = Post.objects.filter(base=b)
        dashboard_object = {'base':b.name , 'member_count':member_count, 'channel_count':channel_count, 'one_week_posts_count': one_week_posts_count, 'compare_posts_count': compare_posts_count,'per_posts':per_posts,'compare_per_posts':compare_per_posts}
        dashboard.append(dashboard_object)
    context = {'dashboards':dashboard}

    return render(request,'analytics/dashboard/base_dashboard.html',context)

class BaseDetailView(generic.DeleteView):
    model = Base

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)


#チャンネル別ダッシュボード
def channel_dashboard(request):
    context = {}
    dashboard = []
    channels = Channel.objects.all()
    for c in channels:
        total_posts = Post.objects.filter(channel=c)
        if total_posts == 0:
            continue
        base = c.base
        one_week_posts = Post.objects.filter(channel=c,created_at__gt=one_week_ago)
        one_week_posts_count = len(one_week_posts)
        two_week_posts = Post.objects.filter(channel=c,created_at__gt=two_week_ago,created_at__lte=one_week_ago)
        two_week_posts_count = len(two_week_posts)
        compare_posts_count = one_week_posts_count-two_week_posts_count
        dashboard_object = {'base':base , 'channel_name':c.name, 'one_week_posts_count': one_week_posts_count,'compare_posts_count': compare_posts_count}
        dashboard.append(dashboard_object)
    context = {'dashboards':dashboard}

    return render(request,'analytics/dashboard/channel_dashboard.html',context)

#メンバー別ダッシュボード
def employee_dashboard(request):
    context = {}
    dashboard = []
    employees = Employee.objects.all()
    for e in employees:
        total_posts = Post.objects.filter(employee=e)
        if total_posts == 0:
            continue
        one_week_posts = Post.objects.filter(employee=e,created_at__gt=one_week_ago)
        one_week_posts_count = len(one_week_posts)
        base = e.base
        two_week_posts = Post.objects.filter(employee=e,created_at__gt=two_week_ago,created_at__lte=one_week_ago)
        two_week_posts_count = len(two_week_posts)
        compare_posts_count = one_week_posts_count-two_week_posts_count
        dashboard_object = {'base':base , 'employee_name':e.name, 'one_week_posts_count': one_week_posts_count,'compare_posts_count': compare_posts_count}
        dashboard.append(dashboard_object)
    context = {'dashboards':dashboard}

    return render(request,'analytics/dashboard/employee_dashboard.html',context)

#メンバー管理関連
class EmployeeListView(generic.ListView):
    template_name = "analytics/employee_list.html"
    model = Employee

class EmployeeCreateView(generic.edit.CreateView):
    model = Employee
    form_class = EmployeeForm
    success_url = reverse_lazy('analytics:employee_index')
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['base_list'] = Base.objects.all()
        return context

    def form_valid(self, form):
        form.save()
        employee_base = form.instance.base
        #所属拠点のチャンネルを全て取得
        channels = Channel.objects.filter(base=employee_base)
        form_instance = form.instance
        unix_three_month_ago = analytics.process.get_time.get_diff_month_ago_unix(3)
        analytics.domain.get_slack_posts(channels,unix_three_month_ago,form_instance)
        unix_two_month_ago = analytics.process.get_time.get_diff_month_ago_unix(2)
        analytics.domain.get_slack_posts(channels,unix_two_month_ago,form_instance)
        unix_one_month_ago = analytics.process.get_time.get_diff_month_ago_unix(1)
        analytics.domain.get_slack_posts(channels,unix_one_month_ago,form_instance)

        return super(EmployeeCreateView, self).form_valid(form)              

#チャンネル管理関連
class ChannelListView(generic.ListView):
    template_name = "analytics/channel_list.html"
    model = Channel

class ChannelCreateView(generic.edit.CreateView):
    model = Channel
    fields = ['name','base','channel_id'] # '__all__'
    success_url = reverse_lazy('analytics:channel_index')

#拠点管理関連
class BaseListView(generic.ListView):
    template_name = "analytics/base_list.html"
    model = Base

class BaseCreateView(generic.edit.CreateView):
    model = Base
    fields = ['name'] # '__all__'
    success_url = reverse_lazy('analytics:base_index')
    def form_valid(self, form):
        return super(BaseCreateView, self).form_valid(form)

#拠点管理関連
class DepartmentListView(generic.ListView):
    template_name = "analytics/department_list.html"
    model = Department

class DepartmentCreateView(generic.edit.CreateView):
    model = Department
    fields = ['name','base'] # '__all__'
    success_url = reverse_lazy('analytics:department_index')
    def form_valid(self, form):
        return super(DepartmentCreateView, self).form_valid(form)