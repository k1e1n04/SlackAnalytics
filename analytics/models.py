from django.db import models
from django.db.models import Q
import analytics.process.gettime as gettime
one_week_ago = gettime.get_diff_days_ago(7)
two_week_ago = gettime.get_diff_days_ago(14)
# Create your models here.

class ModelQuerySet(models.QuerySet):
    def search(self,query=None):
        """EmployeeとChannelをname,base.name,department.nameによって絞り込んだQueryを返す"""
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
        """Departmentをname,base.nameによって絞り込んだQueryを返す"""
        qs = self
        if query is not None:
            or_lookup = (
                Q(name__icontains=query)|
                Q(base__name__icontains=query)
            )
            qs = qs.filter(or_lookup).distinct()
        return qs
    def base_search(self,query=None):
        """Baseをnameによって絞り込んだQueryを返す"""
        qs = self
        if query is not None:
            or_lookup = (
                Q(name__icontains=query)
            )
            qs = qs.filter(or_lookup).distinct()
        return qs

class ModelManager(models.Manager):
    """models.Monagerのget_querysetをオーバーライドするクラス"""
    def get_queryset(self):
        return ModelQuerySet(self.model,using=self._db)
    def search(self,query=None):
        """ModelQuerySetで定義したsearchメソッドを.objects.searchで使えるように紐付け"""
        return self.get_queryset().search(query=query)
    # department用
    def dp_search(self,query=None):
        """ModelQuerySetで定義したdp_searchメソッドを.objects.dp_searchで使えるように紐付け"""
        return self.get_queryset().dp_search(query=query)
    # base用
    def base_search(self,query=None):
        """ModelQuerySetで定義したbase_searchメソッドを.objects.base_searchで使えるように紐付け"""
        return self.get_queryset().base_search(query=query)

class Base(models.Model):
    name = models.CharField(verbose_name="拠点",max_length=50,unique=True)
    objects = ModelManager()
    def base_departments(self):
        """拠点の部署を全て返す"""
        base_departments = Department.objects.filter(base=self)
        return base_departments

    def posts_count_per_department(self):
        """拠点の各部署あたりの投稿数をリストで返す"""
        # 1ヶ月前の日付を取得
        one_month_ago = gettime.get_diff_month_ago(1)
        # 該当メンバーが所属している拠点の部署を全て取得
        base_departments = self.base_departments()
        posts_count_per_department = []
        for department in base_departments:
            channels = Channel.objects.filter(department=department)
            department_posts = Post.objects.filter(base=self,channel__in=channels,created_at__gt=one_month_ago)
            department_posts_count = len(department_posts)
            posts_count_per_department.append([department.name,department_posts_count])
        return posts_count_per_department

    def compare_per_posts(self):
        """直近7日間のメンバーあたりの投稿数とその前の7日間との差分を返す"""
        per_posts = self.per_posts()
        two_week_per_posts = self.two_week_per_posts()
        compare_per_posts = per_posts -two_week_per_posts
        return compare_per_posts

    def two_week_per_posts(self):
        """直近14日前から7日前までの拠点のメンバーあたりの投稿数を返す"""
        two_week_posts_count = self.two_week_posts_count()
        member_count = self.member_count
        try:
            two_week_per_posts = round(two_week_posts_count/member_count)
        except:
            two_week_per_posts = 0
        return two_week_per_posts


    def per_posts(self):
        """直近7日間拠点のメンバーあたりの投稿数を返す"""
        one_week_posts_count = self.one_week_posts_count()
        member_count = self.member_count()
        try:
            per_posts = round(one_week_posts_count/member_count)
        except:
            per_posts = 0
        return per_posts

    def channel_count(self):
        """拠点が所有しているチャンネル数を返す"""
        try:
            channel_count = len(Channel.objects.filter(base=self))
        except:
            channel_count = 0
        return channel_count

    def compare_posts_count(self):
        """直近7日間の拠点全体の投稿数とその前の7日間との差分を返す"""
        two_week_posts_count = self.two_week_posts_count()
        one_week_posts_count = self.one_week_posts_count()
        compare_posts_count = two_week_posts_count - one_week_posts_count
        return compare_posts_count

    def one_week_posts_count(self):
        """直近7日間拠点全体の投稿数を返す"""
        try:
            one_week_posts = Post.objects.filter(base=self,created_at__gt=two_week_ago,created_at__lte=one_week_ago)
            one_week_posts_count = len(one_week_posts)
        except:
            one_week_posts_count = 0
        return  one_week_posts_count
    
    def two_week_posts_count(self):
        """直近14日前から7日前までの拠点全体の投稿数を返す"""
        try:
            two_week_posts = Post.objects.filter(base=self,created_at__gt=two_week_ago,created_at__lte=one_week_ago)
            two_week_posts_count = len(two_week_posts)
        except:
            two_week_posts_count = 0
        return  two_week_posts_count

    def member_count(self):
        """拠点のメンバー数を返す"""
        try:
            member_count = len(Employee.objects.filter(base=self))
        except:
            member_count = 0
        return member_count

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

    def one_week_posts_count(self):
        """直近7日間チャンネル全体の投稿数を返す"""
        one_week_posts = Post.objects.filter(channel=self,created_at__gt=one_week_ago)
        one_week_posts_count = len(one_week_posts)
        return one_week_posts_count

    def two_week_posts_count(self):
        """直近14日前から7日前までのチャネル全体の投稿数を返す"""
        two_week_posts = Post.objects.filter(channel=self,created_at__gt=two_week_ago,created_at__lte=one_week_ago)
        two_week_posts_count = len(two_week_posts)
        return two_week_posts_count

    def compare_posts_count(self):
        """直近7日間のチャンネル全体の投稿数とその前の7日間との差分を返す"""
        two_week_posts_count = self.two_week_posts_count()
        one_week_posts_count = self.one_week_posts_count()
        compare_posts_count = two_week_posts_count - one_week_posts_count
        return compare_posts_count

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

    def base_departments(self):
        """該当メンバーが所属している拠点の部署を全て返す"""
        base_departments = Department.objects.filter(base=self.base)
        return base_departments

    def posts_count_per_department(self):
        """該当メンバーが所属している拠点の各部署あたりの投稿数を返す"""
        # 1ヶ月前の日付を取得
        one_month_ago = gettime.get_diff_month_ago(1)
        # 該当メンバーが所属している拠点の部署を全て取得
        base_departments = self.base_departments()
        posts_count_per_department = []
        for department in base_departments:
            channels = Channel.objects.filter(department=department)
            department_posts = Post.objects.filter(employee=self,channel__in=channels,created_at__gt=one_month_ago)
            department_posts_count = len(department_posts)
            posts_count_per_department.append([department.name,department_posts_count])
        return posts_count_per_department


    def one_week_posts_count(self):
        """直近7日間の該当メンバーの投稿数を返す"""
        one_week_posts = Post.objects.filter(employee=self,created_at__gt=one_week_ago)
        one_week_posts_count = len(one_week_posts)
        return one_week_posts_count

    def two_week_posts_count(self):
        """直近14日前から7日前までの該当メンバーの投稿数を返す"""
        two_week_posts = Post.objects.filter(employee=self,created_at__gt=two_week_ago,created_at__lte=one_week_ago)
        two_week_posts_count = len(two_week_posts)
        return two_week_posts_count

    def compare_posts_count(self):
        """直近7日間の該当メンバーの投稿数とその前の7日間との差分を返す"""
        two_week_posts_count = self.two_week_posts_count()
        one_week_posts_count = self.one_week_posts_count()
        compare_posts_count = two_week_posts_count - one_week_posts_count
        return compare_posts_count

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