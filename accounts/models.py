from django.db import models
from django.contrib.auth.models import PermissionsMixin, UserManager
from django.contrib.auth.base_user import AbstractBaseUser
from django.utils.translation import gettext_lazy as _
from django.utils import timezone
from django.db.models import Q
from analytics.models import Organization
  
class  UserModelQuerySet(models.QuerySet):
    def user_search(self,query=None):
        qs = self
        if query is not None:
            or_lookup = (
                Q(first_name__icontains=query)|
                Q(last_name__icontains=query)|
                Q(base__icontains=query)
            )
            qs = qs.filter(or_lookup).distinct()
        return qs

class CustomUserManager(UserManager):
    use_in_migrations = True
  
    def _create_user(self, password, **extra_fields):
        user = self.model(**extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user
  
    def create_user(self,password=None, **extra_fields):
        extra_fields.setdefault('is_staff', False)
        extra_fields.setdefault('is_superuser', False)
        return self._create_user(password, **extra_fields)
  
    def create_superuser(self,password, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)
  
        if extra_fields.get('is_staff') is not True:
            raise ValueError('Superuser must have is_staff=True.')
        if extra_fields.get('is_superuser') is not True:
            raise ValueError('Superuser must have is_superuser=True.')
        return self._create_user(password, **extra_fields)
    
    def get_queryset(self):
        return UserModelQuerySet(self.model,using=self._db)
    def user_search(self,query=None):
        return self.get_queryset().user_search(query=query)
  
class User(AbstractBaseUser, PermissionsMixin):

  
    username = models.CharField(_('ユーザー名'), max_length=30,unique=True)
    first_name = models.CharField(_('名前'), max_length=30)
    last_name = models.CharField(_('名字'), max_length=150)
    base = models.CharField(_('拠点'), max_length=150)
    organization = models.ForeignKey(
        Organization,
        on_delete=models.CASCADE,
        verbose_name='団体',
        default=1,
    )
  
    is_staff = models.BooleanField(
        _('staff status'),
        default=False,
        help_text=_(
            'Designates whether the user can log into this admin site.'),
    )
    date_joined = models.DateTimeField(_('date joined'), default=timezone.now)
  
    objects = CustomUserManager()
  
    USERNAME_FIELD = 'username'
    REQUIRED_FIELDS = []
  
    class Meta:
        verbose_name = _('user')
        verbose_name_plural = _('users')
  
    def get_full_name(self):
        """管理者ユーザーの苗字と名前をつなげフルネームを返す"""
        full_name = '%s %s' % (self.first_name, self.last_name)
        return full_name.strip()
  
    def get_short_name(self):
        """管理者ユーザーの名前を返す"""
        return self.first_name
