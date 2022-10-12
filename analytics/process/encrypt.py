import base64
from Crypto.Cipher import AES
from django.conf import settings
from Crypto.Util.Padding import pad
from Crypto.Util.Padding import unpad
from Crypto.Random import get_random_bytes


# 環境変数AES_KEYをエンコード
AES_KEY = settings.AES_KEY.encode('utf-8')


def encryption(data):
    """
    AESによる暗号化を行う
    """
    # ランダムの初期化ベクトルの生成
    iv = get_random_bytes(AES.block_size)
    # 受け取ったデータをエンコード
    data = data.encode('utf-8')
    cipher = AES.new(key=AES_KEY, mode=AES.MODE_CBC, iv=iv)
    # 暗号化(パディングする)
    encrypted_data = cipher.encrypt(pad(data, AES.block_size))
    db_data = base64.b64encode(iv + encrypted_data).decode('utf-8')
    return db_data

def decryption(data):
    """
    AESによる復号化を行う
    """
    # dbから読み込んだデータのエンコード
    data = base64.b64decode(data.encode('utf-8'))
    # 初期化ベクトル+暗号化されたデータをそれぞれに分割
    iv = data[:AES.block_size]
    encrypted_data = data[AES.block_size:]
    # 復号
    cipher = AES.new(AES_KEY, AES.MODE_CBC, iv = iv)
    unencrypted_data = unpad(cipher.decrypt(encrypted_data), AES.block_size)
    # デコード
    unencrypted_data = unencrypted_data.decode('utf-8')
    return unencrypted_data



