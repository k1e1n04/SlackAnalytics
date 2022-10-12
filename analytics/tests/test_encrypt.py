from cgi import test
from django.test import TestCase
import analytics.process.encrypt

class TestEncrypt(TestCase):
    """
    AESによる暗号化と復号化が正しく行われるかをテスト
    """
    def test_token_encrypt_case001(self):
        test_data = "xoxp-0000000000000-0000000000000-0000000000000-aa0000a0a0000aaaa00a0000a0aa00000"
        encrypted_data = analytics.process.encrypt.encryption(test_data)
        self.assertNotEqual(encrypted_data,test_data)
        unencrypted_data = analytics.process.encrypt.decryption(encrypted_data)
        self.assertEqual(unencrypted_data,test_data)
