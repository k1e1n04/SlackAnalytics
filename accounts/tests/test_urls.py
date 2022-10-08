from django.test import TestCase
from django.urls import reverse, resolve
from django.contrib.auth import views as auth_views
from ..views import SignUpView,UserList,UserDeleteView, UserUpdateView

# urls.pyをテスト
class TestUserUrls(TestCase):
    # signup ページへのURLでアクセスする時のリダイレクトをテスト"""
  def test_signup_url(self):
    view = resolve('/accounts/signup/')
    self.assertEqual(view.func.view_class, SignUpView)

    # user_list ページへのrootPathでアクセスする時のリダイレクトをテスト"""
  def test_user_list_url(self):
    view = resolve('/accounts/index/')
    self.assertEqual(view.func.view_class, UserList)

    # user_delete ページへのURLでアクセスする時のリダイレクトをテスト"""
  def test_user_delete_url(self):
    view = resolve('/accounts/delete/1/')
    self.assertEqual(view.func.view_class, UserDeleteView)

    # user_update ページへのURLでアクセスする時のリダイレクトをテスト"""
  def test_user_update_url(self):
    view = resolve('/accounts/update/1/')
    self.assertEqual(view.func.view_class, UserUpdateView)

    # password_change_formページへのURLでアクセスする時のリダイレクトをテスト"""
  def test_password_change_form_url(self):
    view = resolve('/accounts/password_change_form/')
    self.assertEqual(view.func.view_class, auth_views.PasswordChangeView)

    # password_change_doneページへのURLでアクセスする時のリダイレクトをテスト"""
  def test_password_change_done_url(self):
    view = resolve('/accounts/password_change_done/')
    self.assertEqual(view.func.view_class, auth_views.PasswordChangeDoneView)
