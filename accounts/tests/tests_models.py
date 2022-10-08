from django.test import TestCase
from accounts.models import User
# Create your tests here.

# userモデルのテスト
class UserModelTests(TestCase):
    # 何も登録されていないことを確かめる
    def test_user_is_empty(self):
        saved_users = User.objects.all()
        self.assertEqual(saved_users.count(), 0)

    # userをひとつ作成した際に正しくカウントされることをテスト
    def test_base_is_count_one(self):
        test_username = "test_username"
        test_first_name = "test_first_name"
        test_last_name = "test_last_name"
        test_base = "test_base"
        user = User(username=test_username,first_name=test_first_name,last_name=test_last_name,base=test_base)
        user.save()
        saved_users = User.objects.all()
        self.assertEqual(saved_users.count(), 1)
    
    # 内容を指定し同じ値が返されることをテスト
    def test_saving_and_retrieving_base(self):
        test_username = "test_username"
        test_first_name = "test_first_name"
        test_last_name = "test_last_name"
        test_base = "test_base"
        user = User(username=test_username,first_name=test_first_name,last_name=test_last_name,base=test_base)
        user.save()
        saved_users = User.objects.all()
        actual_user = saved_users[0]

        self.assertEqual(actual_user.username, test_username)
        self.assertEqual(actual_user.first_name, test_first_name)
        self.assertEqual(actual_user.last_name, test_last_name)
        self.assertEqual(actual_user.base, test_base)
