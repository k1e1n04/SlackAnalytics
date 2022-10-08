from django.test import TestCase
from datetime import datetime,timezone
from analytics.models import Base,Department,Channel,Employee,Post,ModelManager
# Create your tests here.

# ModelManagerのテスト
class ModelMangerTests(TestCase):
    ## searchメソッドを使ってchannelをチャンネル名で絞り込めることを確かめる
    def test_channel_filter_by_name(self):
        base = Base(name="test_base")
        base.save()
        department = Department(name="test_department",base=base)
        department.save()
        channel = Channel(name="test_channel01",channel_id="test_id01",base=base,department=department)
        channel.save()
        channel = Channel(name="test_channel02",channel_id="test_id02",base=base,department=department)
        channel.save()

        #テスト用のクエリ
        query = "test_channel01"
        channels = Channel.objects.search(query=query)
        actual_channel = channels[0]

        self.assertEqual(actual_channel.name, query)

    ## searchメソッドを使ってchannelを拠点名で絞り込めることを確かめる
    def test_channel_filter_by_base(self):
        base01 = Base(name="test_base01")
        base01.save()
        base02 = Base(name="test_base02")
        base02.save()
        department = Department(name="test_department",base=base01)
        department.save()
        channel = Channel(name="test_channel01",channel_id="test_id01",base=base01,department=department)
        channel.save()
        channel = Channel(name="test_channel02",channel_id="test_id02",base=base02,department=department)
        channel.save()

        #テスト用のクエリ
        query = "test_base01"
        channels = Channel.objects.search(query=query)
        actual_channel = channels[0]

        self.assertEqual(actual_channel.base.name, query)
        self.assertEqual(actual_channel.name, "test_channel01")

    ## searchメソッドを使ってchannelを部署名で絞り込めることを確かめる
    def test_channel_filter_by_department(self):
        base01 = Base(name="test_base01")
        base01.save()
        base02 = Base(name="test_base02")
        base02.save()
        department01 = Department(name="test_department01",base=base01)
        department01.save()
        department02 = Department(name="test_department02",base=base02)
        department02.save()
        channel = Channel(name="test_channel01",channel_id="test_id01",base=base01,department=department01)
        channel.save()
        channel = Channel(name="test_channel02",channel_id="test_id02",base=base02,department=department02)
        channel.save()

        #テスト用のクエリ
        query = "test_department02"
        channels = Channel.objects.search(query=query)
        actual_channel = channels[0]

        self.assertEqual(actual_channel.department.name, query)
        self.assertEqual(actual_channel.base.name, "test_base02")
        self.assertEqual(actual_channel.name, "test_channel02")

# Baseモデルのテスト
class BaseModelTests(TestCase):
    # 何も登録されていないことを確かめる
    def test_base_is_empty(self):
        saved_bases = Base.objects.all()
        self.assertEqual(saved_bases.count(), 0)

    # baseをひとつ作成した際に正しくカウントされることをテスト
    def test_base_is_count_one(self):
        base = Base(name="test_base")
        base.save()
        saved_bases = Base.objects.all()
        self.assertEqual(saved_bases.count(), 1)
    
    # 内容を指定し同じ値が返されることをテスト
    def test_saving_and_retrieving_base(self):
        test_base = "test_base"
        base = Base(name=test_base)
        base.save()

        saved_bases = Base.objects.all()
        actual_base = saved_bases[0]

        self.assertEqual(actual_base.name, test_base)

# Baseモデルのメソッドのテスト
class BaseModelMethodTests(TestCase):
    # 部署が一つの場合のテスト
    def test_base_department_normal_case001(self):
        base = Base(name="test_base")
        base.save()
        department = Department(name="test_department",base=base)
        department.save()
        saved_bases = Base.objects.all()
        actual_base = saved_bases[0]
        self.assertEqual(actual_base.base_departments()[0], department)

    # 部署が複数の場合のテスト
    def test_base_department_normal_case002(self):
        base = Base(name="test_base")
        base.save()
        department01 = Department(name="test_department01",base=base)
        department02 = Department(name="test_department02",base=base)
        department01.save()
        department02.save()
        saved_bases = Base.objects.all()
        actual_base = saved_bases[0]


        self.assertEqual(actual_base.base_departments()[0], department01)
        self.assertEqual(actual_base.base_departments()[1], department02)

    # 拠点の部署はゼロだが他拠点に部署があるケース
    def test_base_department_case003(self):
        base01 = Base(name="test_base01")
        base01.save()
        base02 = Base(name="test_base02")
        base02.save()
        department01 = Department(name="test_department01",base=base02)
        department01.save()

        saved_bases = Base.objects.all()
        actual_base = saved_bases[0]
         # 部署が取得されないことをテスト
        self.assertEqual(len(actual_base.base_departments()), 0)


# Departmentモデルのテスト
class DepartmentModelTests(TestCase):
    # 何も登録されていないことを確かめる
    def test_department_is_empty(self):
        saved_departments = Department.objects.all()
        self.assertEqual(saved_departments.count(), 0)

    # departmentをひとつ作成した際に正しくカウントされることをテスト
    def test_department_is_count_one(self):
        base = Base(name="test_base")
        base.save()
        department = Department(name="test_department",base=base)
        department.save()

        saved_departments = Department.objects.all()
        self.assertEqual(saved_departments.count(), 1)
    
    # 内容を指定し同じ値が返されることをテスト
    def test_saving_and_retrieving_department(self):
        test_base = "test_base"
        test_department = "test_department"
        base = Base(name=test_base)
        base.save()
        department = Department(name=test_department,base=base)
        department.save()

        saved_departments = Department.objects.all()
        actual_department = saved_departments[0]

        self.assertEqual(actual_department.name, test_department)
        self.assertEqual(actual_department.base.name, test_base)

# Channelモデルのテスト
class ChannelModelTests(TestCase):
    # 何も登録されていないことを確かめる
    def test_channel_is_empty(self):
        saved_channels = Channel.objects.all()
        self.assertEqual(saved_channels.count(), 0)

    # channelをひとつ作成した際に正しくカウントされることをテスト
    def test_channel_is_count_one(self):
        base = Base(name="test_base")
        base.save()
        department = Department(name="test_department",base=base)
        department.save()
        channel = Channel(name="test_channel",channel_id="test_id",base=base,department=department)
        channel.save()

        saved_channels = Channel.objects.all()
        self.assertEqual(saved_channels.count(), 1)
    
    # 内容を指定し同じ値が返されることをテスト
    def test_saving_and_retrieving_channel(self):
        test_base = "test_base"
        test_department = "test_department"
        test_channel="test_channel"
        test_channel_id="test_channel_id"
        base = Base(name=test_base)
        base.save()
        department = Department(name=test_department,base=base)
        department.save()
        channel = Channel(name=test_channel,channel_id=test_channel_id,base=base,department=department)
        channel.save()

        saved_channels = Channel.objects.all()
        actual_channel = saved_channels[0]

        self.assertEqual(actual_channel.name, test_channel)
        self.assertEqual(actual_channel.channel_id, test_channel_id)
        self.assertEqual(actual_channel.base.name, test_base)
        self.assertEqual(actual_channel.department.name, test_department)

# Employeeモデルのテスト
class EmployeeModelTests(TestCase):
    # 何も登録されていないことを確かめる
    def test_employee_is_empty(self):
        saved_employees = Employee.objects.all()
        self.assertEqual(saved_employees.count(), 0)

    # employeeをひとつ作成した際に正しくカウントされることをテスト
    def test_employee_is_count_one(self):
        base = Base(name="test_base")
        base.save()
        department = Department(name="test_department",base=base)
        department.save()
        channel = Channel(name="test_channel",channel_id="test_id",base=base,department=department)
        channel.save()
        employee = Employee(name="test_employee",slack_id="test_slack_id",base=base,department=department)
        employee.save()

        saved_employees = Employee.objects.all()
        self.assertEqual(saved_employees.count(), 1)
    
    # 内容を指定し同じ値が返されることをテスト
    def test_saving_and_retrieving_channel(self):
        test_base = "test_base"
        test_department = "test_department"
        test_channel="test_channel"
        test_channel_id="test_channel_id"
        test_employee="test_employee"
        test_slack_id="test_slack_id"
        base = Base(name=test_base)
        base.save()
        department = Department(name=test_department,base=base)
        department.save()
        channel = Channel(name=test_channel,channel_id=test_channel_id,base=base,department=department)
        channel.save()
        employee = Employee(name=test_employee,slack_id=test_slack_id,base=base,department=department)
        employee.save()

        saved_employees = Employee.objects.all()
        actual_employee = saved_employees[0]

        self.assertEqual(actual_employee.name, test_employee)
        self.assertEqual(actual_employee.slack_id, test_slack_id)
        self.assertEqual(actual_employee.base.name, test_base)
        self.assertEqual(actual_employee.department.name, test_department)

# Postモデルのテスト
class PostModelTests(TestCase):
    # 何も登録されていないことを確かめる
    def test_post_is_empty(self):
        saved_posts = Post.objects.all()
        self.assertEqual(saved_posts.count(), 0)

    # Postをひとつ作成した際に正しくカウントされることをテスト
    def test_post_is_count_one(self):
        base = Base(name="test_base")
        base.save()
        department = Department(name="test_department",base=base)
        department.save()
        channel = Channel(name="test_channel",channel_id="test_id",base=base,department=department)
        channel.save()
        employee = Employee(name="test_employee",slack_id="test_slack_id",base=base,department=department)
        employee.save()
        post = Post(channel=channel, employee=employee, base=base, created_at=datetime.fromtimestamp(1659279600))
        post.save()
        saved_posts = Post.objects.all()
        self.assertEqual(saved_posts.count(), 1)
    
    # 内容を指定し同じ値が返されることをテスト
    def test_saving_and_retrieving_post(self):
        test_base = "test_base"
        test_department = "test_department"
        test_channel="test_channel"
        test_channel_id="test_channel_id"
        test_employee="test_employee"
        test_slack_id="test_slack_id"
        test_date=datetime.fromtimestamp(1659279600)
        base = Base(name=test_base)
        base.save()
        department = Department(name=test_department,base=base)
        department.save()
        channel = Channel(name=test_channel,channel_id=test_channel_id,base=base,department=department)
        channel.save()
        employee = Employee(name=test_employee,slack_id=test_slack_id,base=base,department=department)
        employee.save()
        post = Post(channel=channel, employee=employee, base=base, created_at=test_date)
        post.save()
        saved_posts = Post.objects.all()

        saved_posts = Post.objects.all()
        actual_post = saved_posts[0]

        self.assertEqual(actual_post.employee.name, test_employee)
        self.assertEqual(actual_post.base.name, test_base)
        self.assertEqual(actual_post.channel.name, test_channel)
        # データベース上はUTCになるので変換
        self.assertEqual(actual_post.created_at, test_date.astimezone(timezone.utc))