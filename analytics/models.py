from django.db import models
from django.db.models import Q

# Create your models here.

class ModelQuerySet(models.QuerySet):
    def search(self,query=None):
        qs = self
        if query is not None:
            or_lookup = (
                Q(name__icontains=query)|
                Q(base__name__icontains=query)|
                Q(department__name__icontains=query)
            )
            qs = qs.filter(or_lookup).distinct()
        return qs
    def dp_search(self,query=None):
        qs = self
        if query is not None:
            or_lookup = (
                Q(name__icontains=query)|
                Q(base__name__icontains=query)
            )
            qs = qs.filter(or_lookup).distinct()
        return qs
    def base_search(self,query=None):
        qs = self
        if query is not None:
            or_lookup = (
                Q(name__icontains=query)
            )
            qs = qs.filter(or_lookup).distinct()
        return qs

class ModelManager(models.Manager):
    def get_queryset(self):
        return ModelQuerySet(self.model,using=self._db)
    def search(self,query=None):
        return self.get_queryset().search(query=query)
    def dp_search(self,query=None):
        return self.get_queryset().dp_search(query=query)
    def base_search(self,query=None):
        return self.get_queryset().base_search(query=query)

class Base(models.Model):
    name = models.CharField(verbose_name="拠点",max_length=50,unique=True)
    objects = ModelManager()
    def __str__(self):
        return self.name

class Department(models.Model):
    name = models.CharField(verbose_name="部署",max_length=50)
    base = models.ForeignKey(
        Base,
        on_delete=models.PROTECT,
        verbose_name='拠点',
    )
    objects = ModelManager()
    def __str__(self):
        return self.name   

class Channel(models.Model):
    name = models.CharField(verbose_name="チャンネル",max_length=50)
    channel_id = models.CharField(verbose_name="チャンネルID",max_length=50,default="",unique=True)
    base = models.ForeignKey(
        Base,
        on_delete=models.PROTECT,
        verbose_name='拠点',
    )
    department = models.ForeignKey(
        Department,
        on_delete=models.PROTECT,
        verbose_name='部署',
        default="",
    )
    objects = ModelManager()
    def __str__(self):
        return self.name


class Employee(models.Model):
    name = models.CharField(verbose_name="名前",max_length=30)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    slack_id = models.CharField(verbose_name="SlackID",max_length=30,unique=True)
    base = models.ForeignKey(
        Base,
        on_delete=models.PROTECT,
        verbose_name='拠点',
    )
    department = models.ForeignKey(
        Department,
        on_delete=models.PROTECT,
        verbose_name='部署',
    )
    objects = ModelManager()
    def __str__(self):
        return self.name


class Post(models.Model):
    channel = models.ForeignKey(
        Channel,
        on_delete=models.PROTECT,
        verbose_name='チャンネル',
    )
    employee = models.ForeignKey(
        Employee,
        on_delete=models.CASCADE,
        verbose_name='メンバー',
    )
    base = models.ForeignKey(
        Base,
        on_delete=models.PROTECT,
        verbose_name='拠点',
        default="",
    )
    created_at = models.DateTimeField(verbose_name="投稿日時")
    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=["channel", "created_at"],
                name="channel_date_unique"
            ),
        ]
    def __str__(self):
        return self.channel.name