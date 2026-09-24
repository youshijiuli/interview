import os
server_name = 'server'
db_name = 'db'
home = 'home'
# 项目服务器文件路径
PROJECT_SERVER_PATH = os.path.dirname(os.path.dirname(__file__))
# 服务端 db 文件夹路径
SERVER_DB_PATH = os.path.join(PROJECT_SERVER_PATH,db_name)
SERVER_HOME_PATH = os.path.join(PROJECT_SERVER_PATH,home)