import os,sys
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.append(BASE_DIR)
ip_port = ('127.0.0.1',8080)
recv_size = 1024
listen_size = 5
path_account_info = os.path.join(BASE_DIR,'conf','account_info.ini')

# print(path_account_info)
# import hashlib
# # print(hashlib.md5('123'.encode('utf-8')).hexdigest())