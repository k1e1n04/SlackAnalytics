from django.test import TestCase
from django.urls import reverse, resolve
from ..views import BaseDashboard,ChannelDashboard,EmployeeDashboard,EmployeeDetailDashboard,BaseCreateView,BaseDetailDashboard,BaseListView,DepartmentCreateView,DepartmentDeleteView,DepartmentListView,DepartmentUpdateView,EmployeeCreateView,EmployeeDeleteView,EmployeeListView,EmployeeUpdateView,ChannelCreateView,ChannelDeleteView,ChannelListView,ChannelUpdateView

# urls.pyをテスト
class TestUrls(TestCase):
    # base_dashboard ページへのURLでアクセスする時のリダイレクトをテスト"""
  def test_basedashboard_url(self):
    view = resolve('/basedashboard/')
    self.assertEqual(view.func.view_class, BaseDashboard)

    # base_dashboard ページへのrootPathでアクセスする時のリダイレクトをテスト"""
  def test_basedashboard_root_url(self):
    view = resolve('/')
    self.assertEqual(view.func.view_class, BaseDashboard)

    # BaseDetailDashboardページへアクセスする時のリダイレクトをテスト"""
  def test_basedetaildashboard_url(self):
    view = resolve('/basedashboard/1')
    self.assertEqual(view.func.view_class, BaseDetailDashboard)

    # channel_dashboard ページへのURLでアクセスする時のリダイレクトをテスト"""
  def test_channeldashboard_url(self):
    view = resolve('/channeldashboard/')
    self.assertEqual(view.func.view_class, ChannelDashboard)

    # employee_dashboard ページへのURLでアクセスする時のリダイレクトをテスト"""
  def test_employeedashboard_url(self):
    view = resolve('/employeedashboard/')
    self.assertEqual(view.func.view_class, EmployeeDashboard)

    # employee_detail_dashboard ページへのURLでアクセスする時のリダイレクトをテスト"""
  def test_employeedetaildashboard_url(self):
    view = resolve('/employeedashboard/1')
    self.assertEqual(view.func.view_class, EmployeeDetailDashboard)

    # base_indexページへのURLでアクセスする時のリダイレクトをテスト"""
  def test_base_index_url(self):
    view = resolve('/base/index/')
    self.assertEqual(view.func.view_class, BaseListView)

    # base_createページへのURLでアクセスする時のリダイレクトをテスト"""
  def test_base_create_url(self):
    view = resolve('/base/create/')
    self.assertEqual(view.func.view_class, BaseCreateView)

    # department_indexページへのURLでアクセスする時のリダイレクトをテスト"""
  def test_department_index_url(self):
    view = resolve('/department/index/')
    self.assertEqual(view.func.view_class, DepartmentListView)

    # department_createページへのURLでアクセスする時のリダイレクトをテスト"""
  def test_department_create_url(self):
    view = resolve('/department/create/')
    self.assertEqual(view.func.view_class, DepartmentCreateView)

    # department_updateページへのURLでアクセスする時のリダイレクトをテスト"""
  def test_department_update_url(self):
    view = resolve('/department/update/1/')
    self.assertEqual(view.func.view_class, DepartmentUpdateView)

    # department_deleteページへのURLでアクセスする時のリダイレクトをテスト"""
  def test_department_delete_url(self):
    view = resolve('/department/delete/1/')
    self.assertEqual(view.func.view_class, DepartmentDeleteView)

    # employee_indexページへのURLでアクセスする時のリダイレクトをテスト"""
  def test_employee_index_url(self):
    view = resolve('/employee/index/')
    self.assertEqual(view.func.view_class, EmployeeListView)

    # employee_createページへのURLでアクセスする時のリダイレクトをテスト"""
  def test_employee_create_url(self):
    view = resolve('/employee/create/')
    self.assertEqual(view.func.view_class, EmployeeCreateView)

    # employee_updateページへのURLでアクセスする時のリダイレクトをテスト"""
  def test_employee_update_url(self):
    view = resolve('/employee/update/1/')
    self.assertEqual(view.func.view_class, EmployeeUpdateView)

    # employee_deleteページへのURLでアクセスする時のリダイレクトをテスト"""
  def test_employee_delete_url(self):
    view = resolve('/employee/delete/1/')
    self.assertEqual(view.func.view_class, EmployeeDeleteView)

    # channel_indexページへのURLでアクセスする時のリダイレクトをテスト"""
  def test_channel_index_url(self):
    view = resolve('/channel/index/')
    self.assertEqual(view.func.view_class, ChannelListView)

    # channel_createページへのURLでアクセスする時のリダイレクトをテスト"""
  def test_channel_create_url(self):
    view = resolve('/channel/create/')
    self.assertEqual(view.func.view_class, ChannelCreateView)

    # channel_updateページへのURLでアクセスする時のリダイレクトをテスト"""
  def test_channel_update_url(self):
    view = resolve('/channel/update/1/')
    self.assertEqual(view.func.view_class, ChannelUpdateView)

    # channel_deleteページへのURLでアクセスする時のリダイレクトをテスト"""
  def test_channel_delete_url(self):
    view = resolve('/channel/delete/1/')
    self.assertEqual(view.func.view_class, ChannelDeleteView)

