from audioop import reverse
from django.shortcuts import render
from django.contrib.auth.forms import PasswordChangeForm
from django.urls import reverse_lazy
from django .views import generic
from .models import User
from django.contrib.auth.mixins import LoginRequiredMixin,UserPassesTestMixin
from django.contrib.auth.views import PasswordChangeView,PasswordChangeDoneView,PasswordContextMixin
import logging
from .forms import (
    UserCreateForm,
    UserUpdateForm
)
# Loggerの取得
logger = logging.getLogger('accounts')

class OnlyYouMixin(UserPassesTestMixin):
    """管理者ユーザー自分自身でないとアクセスできないようにするためのMxin"""
    raise_exception = False

    def test_func(self):
        user = self.request.user
        logger.debug("OnlyYouMixin called by a member of {}".format(user.organization))
        return user.pk == self.kwargs['pk'] or user.is_staff

class OnlyYourOrganizationMixin(UserPassesTestMixin):
    """管理者ユーザー自分自身のOrganizationと変更対象のUserのOrganizationが一致するときだけアクセスを許可するMxin"""
    raise_exception = False

    def test_func(self):
        current_user = self.request.user
        user = User.objects.filter(pk=self.kwargs['pk']).first()
        logger.debug("OnlyYourOrganizationMixin called by {}".format(current_user))
        if current_user.organization != user.organization:
            logger.warning("A member of {} tried to watch the informations of a member of {}".format(current_user.organization,user.organization))
        return current_user.organization == user.organization

# Create your views here.
class SignUpView(LoginRequiredMixin,generic.CreateView):
    """管理者ユーザー登録画面\n
    ユーザー名(ログイン用)、苗字、名前、拠点、仮パスワードを入力し管理者ユーザーを作成する\n
    ここで登録したユーザー名とパスワードを本人に伝える\n
    ユーザー名とパスワードは必ず変更する
    """
    logger.debug("SignUpView called")
    form_class = UserCreateForm
    success_url = reverse_lazy('analytics:base_dashboard')
    template_name = 'accounts/signup.html'
    def form_valid(self, form):
        current_user = self.request.user
        logger.info("Created new user of {}".format(current_user.organization))
        form.instance.organization = current_user.organization
        return super(SignUpView, self).form_valid(form)

class UserList(LoginRequiredMixin,generic.ListView):
    """管理者ユーザー一覧画面\n
    ユーザー名、拠点名、スタッフ権限を確認することができる\n
    管理ユーザーの削除画面や登録画面に遷移することができる
    """
    logger.debug("UserList called")
    template_name = "accounts/user_list.html"
    def get_queryset(self):
        current_user = self.request.user
        logger.debug("UserList called by a member of {}".format(current_user.organization))
        try:
            query= self.request.GET.get('query')
        except:
            query = None
        logger.debug("query '{}' was seted".format(query))
        users = User.objects.user_search(query=query).filter(organization=current_user.organization)
        return users

class UserDeleteView(OnlyYourOrganizationMixin,generic.DeleteView):
    """管理者ユーザー削除画面\n
    管理者ユーザーの一覧画面から削除ボタンを押しすと遷移できる\n
    本当に削除して良いかの確認を行う\n
    """
    logger.debug("UserDeleteView called")
    model = User
    template_name = "accounts/user_delete.html"
    success_url = reverse_lazy('accounts:index')

class UserUpdateView(OnlyYouMixin,generic.UpdateView):
    """管理者ユーザー情報更新画面\n
    nav-barに表示されている自分の名前から遷移することができる/n
    ユーザー名、苗字、名前の変更ができる他、パスワード変更ページへ遷移できる\n
    本人のみがアクセス可能
    """
    logger.debug("UserUpdateView called")
    model = User
    form_class = UserUpdateForm
    success_url = reverse_lazy('analytics:base_dashboard')
    template_name = 'accounts/update.html'

class PasswordChangeView(OnlyYouMixin,PasswordContextMixin, generic.FormView):
    """
    管理者ユーザーパスワード変更画面/n
    本人のみがアクセス可能
    """
    logger.debug("PasswordChangeView called")
    form_class = PasswordChangeForm
    success_url = reverse_lazy('password_change_done')
    template_name = 'registration/password_change_form.html'
    title = 'Password change'

class PasswordChangeDoneView(PasswordContextMixin, generic.TemplateView):
    """
    管理者ユーザーパスワード変更完了画面
    """
    logger.debug("PasswordChangeDoneView called")
    template_name = 'registration/password_change_done.html'
    title = 'Password change successful'