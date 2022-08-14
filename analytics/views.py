from curses.ascii import EM
from email import contentmanager
from django.views import generic
from .forms import EmployeeForm
from .models import Base,Department,Channel,Employee,Post
from django.views import generic
from django.urls import reverse_lazy
import analytics.domain
import analytics.process.get_time
from django.contrib.auth.mixins import LoginRequiredMixin

one_week_ago = analytics.process.get_time.get_diff_days_ago(7)
two_week_ago = analytics.process.get_time.get_diff_days_ago(14)

#拠点別ダッシュボード
class base_dashboard(LoginRequiredMixin,generic.TemplateView):
    template_name = "analytics/dashboard/base_dashboard.html"
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        dashboard = []
        bases = Base.objects.all()
        for b in bases:
            member_count = len(Employee.objects.filter(base=b))
            if member_count == 0:
                continue
            one_week_posts = Post.objects.filter(base=b,created_at__gt=one_week_ago)
            two_week_posts = Post.objects.filter(base=b,created_at__gt=two_week_ago,created_at__lte=one_week_ago)
            one_week_posts_count,compare_posts_count,two_week_posts_count = analytics.domain.return_compare_posts_conut(one_week_posts,two_week_posts)
            per_posts = round(one_week_posts_count/member_count)
            compare_per_posts = round(per_posts-(two_week_posts_count/member_count))
            channel_count = len(Channel.objects.filter(base=b))
            total_posts = Post.objects.filter(base=b)
            dashboard_object = {'base':b.name , 'member_count':member_count, 'channel_count':channel_count, 'one_week_posts_count': one_week_posts_count, 'compare_posts_count': compare_posts_count,'per_posts':per_posts,'compare_per_posts':compare_per_posts}
            dashboard.append(dashboard_object)
        context['dashboards'] = dashboard
        return context

class BaseDetailView(LoginRequiredMixin,generic.DeleteView):
    model = Base

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)


#チャンネル別ダッシュボード
class channel_dashboard(LoginRequiredMixin,generic.TemplateView):
    template_name = 'analytics/dashboard/channel_dashboard.html'
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        dashboard = []
        channels = Channel.objects.all()
        for c in channels:
            total_posts = Post.objects.filter(channel=c)
            if total_posts == 0:
                continue
            base = c.base
            department = c.department
            one_week_posts = Post.objects.filter(channel=c,created_at__gt=one_week_ago)
            two_week_posts = Post.objects.filter(channel=c,created_at__gt=two_week_ago,created_at__lte=one_week_ago)
            one_week_posts_count,compare_posts_count,two_week_posts_count = analytics.domain.return_compare_posts_conut(one_week_posts,two_week_posts)
            dashboard_object = {'base':base , 'channel_name':c.name, 'department':c.department, 'one_week_posts_count': one_week_posts_count,'compare_posts_count': compare_posts_count}
            dashboard.append(dashboard_object)
        context['dashboards'] = dashboard
        return context

#メンバー別ダッシュボード
class employee_dashboard(LoginRequiredMixin,generic.TemplateView):
    template_name = "analytics/dashboard/employee_dashboard.html"
    def get_context_data(self,**kwargs):
        context = super().get_context_data(**kwargs)
        dashboard = []
        employees = Employee.objects.all()
        for e in employees:
            total_posts = Post.objects.filter(employee=e)
            if total_posts == 0:
                continue
            base = e.base
            department = e.department
            one_week_posts = Post.objects.filter(employee=e,created_at__gt=one_week_ago)
            two_week_posts = Post.objects.filter(employee=e,created_at__gt=two_week_ago,created_at__lte=one_week_ago)
            one_week_posts_count,compare_posts_count,two_week_posts_count = analytics.domain.return_compare_posts_conut(one_week_posts,two_week_posts)
            dashboard_object = {'base':base , 'employee_id':e.pk,'employee_name':e.name, 'department':department, 'one_week_posts_count': one_week_posts_count,'compare_posts_count': compare_posts_count}
            dashboard.append(dashboard_object)
        context['dashboards'] = dashboard
        return context

class employee_detail_dashboard(LoginRequiredMixin,generic.DetailView):
    model = Employee
    context_object_name = "employee_detail"
    template_name = "analytics/dashboard/employee_detail_dashboard.html"
    def get_context_data(self,**kwargs):
        context = super().get_context_data(**kwargs)
        employee = context.get('object')
        one_week_posts = Post.objects.filter(employee=employee,created_at__gt=one_week_ago)
        two_week_posts = Post.objects.filter(employee=employee,created_at__gt=two_week_ago,created_at__lte=one_week_ago)
        one_week_posts_count,compare_posts_count,two_week_posts_count = analytics.domain.return_compare_posts_conut(one_week_posts,two_week_posts)

        departments = Department.objects.filter(base=employee.base)
        one_month_ago = analytics.process.get_time.get_diff_month_ago(1)
        departments_posts_count = analytics.domain.return_departments_posts_count(departments,employee,one_month_ago)
        dashboard_object = {'one_week_posts_count': one_week_posts_count,'compare_posts_count': compare_posts_count}
        context['departments'] = departments
        context['departments_post_data'] = departments_posts_count
        context['dashboard'] = dashboard_object
        return context

#メンバー管理関連
class EmployeeListView(LoginRequiredMixin,generic.ListView):
    template_name = "analytics/employee_list.html"
    model = Employee

class EmployeeCreateView(LoginRequiredMixin,generic.edit.CreateView):
    model = Employee
    form_class = EmployeeForm
    success_url = reverse_lazy('analytics:employee_index')
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['base_list'] = Base.objects.all()
        return context

    def form_valid(self, form):
        form.save()
        return super(EmployeeCreateView, self).form_valid(form)

class EmployeeUpdateView(LoginRequiredMixin,generic.UpdateView):
    model = Employee
    form_class = EmployeeForm
    template_name = "analytics/employee_update.html"
    success_url = reverse_lazy("analytics:employee_index")

class EmployeeDeleteView(LoginRequiredMixin,generic.DeleteView):
    model = Employee
    template_name = "analytics/delete.html"
    success_url = reverse_lazy("analytics:employee_index")


#チャンネル管理関連
class ChannelListView(LoginRequiredMixin,generic.ListView):
    template_name = "analytics/channel_list.html"
    model = Channel

class ChannelCreateView(LoginRequiredMixin,generic.edit.CreateView):
    model = Channel
    fields = ['name','base','department','channel_id'] # '__all__'
    success_url = reverse_lazy('analytics:channel_index')
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['base_list'] = Base.objects.all()
        return context

#拠点管理関連
class BaseListView(LoginRequiredMixin,generic.ListView):
    template_name = "analytics/base_list.html"
    model = Base

class BaseCreateView(LoginRequiredMixin,generic.edit.CreateView):
    model = Base
    fields = ['name'] # '__all__'
    success_url = reverse_lazy('analytics:base_index')
    def form_valid(self, form):
        return super(BaseCreateView, self).form_valid(form)

#拠点管理関連
class DepartmentListView(LoginRequiredMixin,generic.ListView):
    template_name = "analytics/department_list.html"
    model = Department

class DepartmentCreateView(LoginRequiredMixin,generic.edit.CreateView):
    model = Department
    fields = ['name','base'] # '__all__'
    success_url = reverse_lazy('analytics:department_index')
    def form_valid(self, form):
        return super(DepartmentCreateView, self).form_valid(form)