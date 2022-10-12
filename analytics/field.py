import analytics.process.encrypt as encrypt
from django.db import models

class EncryptedFieldMixin:
    """
    Djangoのモデルフィールドを、DB登録時に暗号化するように
    変更するMixin
    戻り値が str のため、models.BinaryFieldなどには使えない
    """

    def pre_save(self, model_instance, add):
        """
        model_instance がもつフィールドの値を暗号化する
        """
        value = getattr(model_instance, self.attname)
        ret = encrypt.encryption(value)
        return ret

    def from_db_value(self, encrypted_text, expression, connection):
        """
        DBから取り出したフィールドの値を復号化する
        """
        if encrypted_text is None:
            return encrypted_text
        try:
            return encrypt.decryption(encrypted_text)
        except ValueError:
            return encrypted_text


class EncryptedTextField(EncryptedFieldMixin, models.TextField):
    """
    データをDB登録時に自動で暗号化するフィールド
    TextFieldを継承しているため、ModelAdminやModelFormでも
    TextFieldと同じように使える。
    マイグレーションファイルは生成されるが DBのデータ型は同じため、
    既存のTextFieldとの置き換えが可能。
    """
    pass
