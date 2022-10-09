from django.views import generic
from .forms import EmployeeForm
from .models import Base,Department,Channel,Employee
from django.views import generic
from django.urls import reverse_lazy
import analytics.domain
import analytics.process.gettime as gettime
from django.contrib.auth.mixins import LoginRequiredMixin

#　1週間前の日付を取得
one_week_ago = gettime.get_diff_days_ago(7)
#　2週間前の日付を取得
two_week_ago = gettime.get_diff_days_ago(14)

#自分が所属している拠点のサマリー
class SummaryView(LoginRequiredMixin,generic.TemplateView):
    """自拠点のサマリー\n
    
    """
    template_name = "analytics/summary/summary.html"
    def get_context_data(self, **kwargs):
        context= super().get_context_data(**kwargs)
        base = Base.objects.filter(name=self.request.user.base).first()
        next_monday = gettime.get_next_monday()
        dateList,str_dateList = gettime.six_month_dateList(next_monday)
        post_date_list = analytics.domain.getGoogleChartPosts(dateList,str_dateList,base=base)
        context['postDateList'] = post_date_list
        context['base'] = base
        return context

#拠点別ダッシュボード
class BaseDashboard(LoginRequiredMixin,generic.ListView):
    """拠点一覧のダッシュボード\n
    拠点名、チャンネル数、メンバー数、直近7日間の投稿数、直近7日間のメンバーあたりの平均投稿数を表示\n
    拠点名で検索し絞り込むことができる
    """
    template_name = "analytics/dashboard/base_dashboard.html"
    def get_queryset(self):
        try:
            query= self.request.GET.get('query')
        except:
            query = None
        bases = Base.objects.base_search(query=query)
        return bases

# 拠点の詳細ダッシュボード
class BaseDetailDashboard(LoginRequiredMixin,generic.DetailView):
    """任意の拠点の詳細ダッシュボード\n
    拠点名、チャンネル数、メンバー数、直近7日間の投稿数(先週比)、直近7日間のメンバーあたりの平均投稿数(先週比)
    に加え、直近30日間の部署別投稿比率の円グラフ、直近半年間の拠点の週あたり投稿数の推移の折れ線グラフを表示
    """
    model = Base
    context_object_name = "base_detail"
    template_name = "analytics/dashboard/base_detail_dashboard.html"
    def get_context_data(self, **kwargs):
        context= super().get_context_data(**kwargs)
        base = context.get('object')
        next_monday = gettime.get_next_monday()
        dateList,str_dateList = gettime.six_month_dateList(next_monday)
        post_date_list = analytics.domain.getGoogleChartPosts(dateList,str_dateList,base=base)
        context['postDateList'] = post_date_list
        return context


#チャンネル別ダッシュボード
class ChannelDashboard(LoginRequiredMixin,generic.ListView):
    """Slackのチャンネル一覧のダッシュボード\n
    チャンネル数、拠点名、部署名、直近7日間の投稿数(先週比)を表示\n
    チャンネル名、拠点名、部署名で絞り込むことができる
    """
    template_name = 'analytics/dashboard/channel_dashboard.html'
    def get_queryset(self):
        try:
            query= self.request.GET.get('query')
        except:
            query = None
        channels = Channel.objects.search(query=query).order_by("name")
        return channels

#メンバー別ダッシュボード
class EmployeeDashboard(LoginRequiredMixin,generic.ListView):
    """メンバー一覧のダッシュボード\n
    メンバー名、拠点名、部署名、直近7日間の投稿数(先週比)を表示\n
    メンバー名、拠点名、部署名で絞り込むことができる
    """
    template_name = "analytics/dashboard/employee_dashboard.html"
    def get_queryset(self):
        try:
            query= self.request.GET.get('query')
        except:
            query = None
        employees = Employee.objects.search(query=query)
        employees = sorted(employees, key=lambda employee: employee.one_week_posts_count(),reverse=True)
        return employees

class EmployeeDetailDashboard(LoginRequiredMixin,generic.DetailView):
    """任意のメンバーの詳細ダッシュボード\n
    メンバー名、拠点名、部署名、直近7日間の投稿数(先週比)
    に加え、直近30日間の部署別投稿比率の円グラフ、直近半年間の拠点の週あたり投稿数の推移の折れ線グラフを表示
    """
    model = Employee
    context_object_name = "employee_detail"
    template_name = "analytics/dashboard/employee_detail_dashboard.html"
    def get_context_data(self,**kwargs):
        context = super().get_context_data(**kwargs)
        employee = context.get('object')
        next_monday = gettime.get_next_monday()
        dateList,str_dateList = gettime.six_month_dateList(next_monday)
        post_date_list = analytics.domain.getGoogleChartPosts(dateList,str_dateList,employee=employee)
        context['postDateList'] = post_date_list
        return context

#メンバー管理関連
class EmployeeListView(LoginRequiredMixin,generic.ListView):
    """メンバー管理画面\n
    メンバーを新たに登録する画面、任意のメンバーの情報更新や削除画面に遷移できる\n
    メンバー名、拠点名、部署名で絞り込むことができる
    """
    template_name = "analytics/employee/employee_list.html"
    def get_queryset(self):
        try:
            query= self.request.GET.get('query')
        except:
            query = None
        employees = Employee.objects.search(query=query)
        return employees

class EmployeeCreateView(LoginRequiredMixin,generic.edit.CreateView):
    """メンバー登録画面\n
    名前、拠点、部署名を登録し、メンバーを新たに作成する\n
    全ての項目の入力は必須\n
    拠点を選択すると部署は自動で絞り込まれる
    """
    model = Employee
    template_name = "analytics/employee/employee_form.html"
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
    """メンバー情報更新画面\n
    名前、拠点、部署名を更新することができる\n
    全ての項目の入力は必須\n
    拠点を選択すると部署は自動で絞り込まれる
    """
    model = Employee
    fields = ['name','base','department']
    template_name = "analytics/update.html"
    success_url = reverse_lazy("analytics:employee_index")

class EmployeeDeleteView(LoginRequiredMixin,generic.DeleteView):
    """メンバー削除画面\n
    メンバー管理の一覧画面から削除ボタンを押しすと遷移できる\n
    本当に削除して良いかの確認を行う
    """
    model = Employee
    template_name = "analytics/delete.html"
    success_url = reverse_lazy("analytics:employee_index")


#チャンネル管理関連
class ChannelListView(LoginRequiredMixin,generic.ListView):
    """チャンネル管理画面\n
    Slackのチャンネルを新たに登録する画面、任意のチャンネルの情報更新や削除画面に遷移できる\n
    チャンネル名、拠点名、部署名で絞り込むことができる
    """
    template_name = "analytics/channel/channel_list.html"
    def get_queryset(self):
        try:
            query= self.request.GET.get('query')
        except:
            query = None
        channels = Channel.objects.order_by("name").search(query=query)
        return channels

class ChannelCreateView(LoginRequiredMixin,generic.edit.CreateView):
    """チャンネル登録画面\n
    チャンネル名、拠点名、部署名を更新することができる\n
    全ての項目の入力は必須\n
    拠点を選択すると部署は自動で絞り込まれる
    """
    model = Channel
    template_name = "analytics/channel/channel_form.html"
    fields = ['name','base','department','channel_id'] # '__all__'
    success_url = reverse_lazy('analytics:channel_index')
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['base_list'] = Base.objects.all()
        return context

class ChannelUpdateView(LoginRequiredMixin,generic.UpdateView):
    """チャンネル情報更新画面\n
    チャンネル名、拠点、部署、SlackチャンネルIDを登録し、チャンネルを新たに作成する\n
    全ての項目の入力は必須\n
    拠点を選択すると部署は自動で絞り込まれる
    """
    model = Channel
    template_name = "analytics/update.html"
    success_url = reverse_lazy("analytics:channel_index")
    fields = '__all__'

class ChannelDeleteView(LoginRequiredMixin,generic.DeleteView):
    """チャンネル削除画面\n
    チャンネル管理の一覧画面から削除ボタンを押しすと遷移できる\n
    本当に削除して良いかの確認を行う
    """
    model = Channel
    template_name = "analytics/delete.html"
    success_url = reverse_lazy("analytics:channel_index")

#拠点管理関連
class BaseListView(LoginRequiredMixin,generic.ListView):
    """拠点管理画面\n
    拠点を新たに登録する画面、任意の拠点の情報更新や削除画面に遷移できる\n
    拠点名で絞り込むことができる
    """
    template_name = "analytics/base/base_list.html"
    def get_queryset(self):
        try:
            query= self.request.GET.get('query')
        except:
            query = None
        bases = Base.objects.base_search(query=query)
        return bases


class BaseCreateView(LoginRequiredMixin,generic.edit.CreateView):
    """拠点登録画面\n
    拠点名を登録し、拠点を新たに作成する\n
    全ての項目の入力は必須
    """
    model = Base
    template_name = "analytics/base/base_form.html"
    fields = ['name']
    success_url = reverse_lazy('analytics:base_index')
    def form_valid(self, form):
        return super(BaseCreateView, self).form_valid(form)

#部署管理関連
class DepartmentListView(LoginRequiredMixin,generic.ListView):
    """部署管理画面\n
    部署を新たに登録する画面、任意の部署の情報更新や削除画面に遷移できる\n
    拠点名、部署名で絞り込むことができる
    """
    template_name = "analytics/department/department_list.html"
    def get_queryset(self):
        try:
            query= self.request.GET.get('query')
        except:
            query = None
        departments = Department.objects.dp_search(query=query)
        return departments

class DepartmentCreateView(LoginRequiredMixin,generic.edit.CreateView):
    """部署登録画面\n
    部署名、拠点を登録し、部署を新たに作成する\n
    全ての項目の入力は必須
    """
    model = Department
    template_name = "analytics/department/department_form.html"
    fields = ['name','base'] # '__all__'
    success_url = reverse_lazy('analytics:department_index')
    def form_valid(self, form):
        return super(DepartmentCreateView, self).form_valid(form)

class DepartmentUpdateView(LoginRequiredMixin,generic.UpdateView):
    """部署情報更新画面\n
    部署名、拠点名を更新することができる\n
    全ての項目の入力は必須
    """
    model = Department
    template_name = "analytics/update.html"
    success_url = reverse_lazy("analytics:department_index")
    fields = '__all__'

class DepartmentDeleteView(LoginRequiredMixin,generic.DeleteView):
    """部署削除画面\n
    部署管理の一覧画面から削除ボタンを押しすと遷移できる\n
    本当に削除して良いかの確認を行う
    """
    model = Department
    template_name = "analytics/delete.html"
    success_url = reverse_lazy("analytics:department_index")