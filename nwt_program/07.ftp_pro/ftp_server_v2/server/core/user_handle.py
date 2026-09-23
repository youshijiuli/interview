import os,sys,pickle,hashlib
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.append(BASE_DIR)
from conf import settings
import configparser


class UserHandle:
    def __init__(self,username):
        self.username= username
        self.config = configparser.ConfigParser()
        self.config.read(settings.path_account_info)

    def judge(self):
        """判断用户是否存在"""
        if self.config.has_section(self.username):
            print('判断用户是否存在')
            return self.config.items(self.username)

