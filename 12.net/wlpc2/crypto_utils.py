from Crypto.Cipher import AES, PKCS1_OAEP
from Crypto.PublicKey import RSA
from Crypto.Random import get_random_bytes
import base64
import os

class CryptoUtils:
    @staticmethod
    def generate_rsa_keys():
        key = RSA.generate(2048)
        private_key = key.export_key()
        public_key = key.publickey().export_key()
        return private_key, public_key

    @staticmethod
    def encrypt_with_rsa(public_key, data):
        rsa_key = RSA.import_key(public_key)
        cipher_rsa = PKCS1_OAEP.new(rsa_key)
        return cipher_rsa.encrypt(data)

    @staticmethod
    def decrypt_with_rsa(private_key, encrypted_data):
        rsa_key = RSA.import_key(private_key)
        cipher_rsa = PKCS1_OAEP.new(rsa_key)
        return cipher_rsa.decrypt(encrypted_data)

    @staticmethod
    def generate_aes_key():
        return get_random_bytes(16)

    @staticmethod
    def encrypt_with_aes(key, data):
        iv = get_random_bytes(16)
        cipher = AES.new(key, AES.MODE_CFB, iv)
        ciphertext = cipher.encrypt(data)
        return base64.b64encode(iv + ciphertext)

    @staticmethod
    def decrypt_with_aes(key, encrypted_data):
        encrypted_data = base64.b64decode(encrypted_data)
        iv = encrypted_data[:16]
        ciphertext = encrypted_data[16:]
        cipher = AES.new(key, AES.MODE_CFB, iv)
        return cipher.decrypt(ciphertext)

    @staticmethod
    def calculate_encrypted_size(data_size):
        """计算AES加密后的大小"""
        # AES块大小是16字节
        block_size = 16
        # 加密后大小 = 原始大小 + (块大小 - 原始大小 % 块大小) + IV大小(16字节)
        if data_size % block_size == 0:
            return data_size + block_size + 16  # 添加一个完整块作为填充 + IV
        else:
            return data_size + (block_size - data_size % block_size) + 16

    @staticmethod
    def calc_encrypted_len(plain_len):
        """计算AES加密后的数据长度"""
        block_size = 16
        # 计算填充后的长度
        padded_len = plain_len + (block_size - plain_len % block_size)
        # 增加IV长度
        return padded_len + block_size  # IV(16) + 加密数据