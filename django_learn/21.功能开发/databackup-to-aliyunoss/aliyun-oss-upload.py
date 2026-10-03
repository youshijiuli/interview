# -*- coding: utf-8 -*-

"""
    实现的功能点如下：
    1. 列出相关现有的项目目录(在权限访问内)
    @. 暂时关掉写的权限，比如创建相关业务目录，在细分MySQL，MongoDB等不同的数据库
    @. 暂时关闭压缩备份文件的功能，在各个项目中shell来实现
    2. 上传到制定目录(检查文件是否压缩)

    使用方法 xxx.py objectName localfilePath projectName
    objectname:  delta/mysql/sql.zip
    localfilepath:  /opt/backup/mysql/sql.zip
    projectName: yiban
"""

import os,sys,zipfile
import oss2
import configparser
import requests
import json
import datetime,time

# 显示上传百分比，任务后台执行则可不用
# def percentage(consumed_bytes, total_bytes):
#     if total_bytes:
#         rate = int(100 * (float(consumed_bytes) / float(total_bytes)))
#         print('\r{0}% '.format(rate), end=)
#         sys.stdout.flush()

# 微信机器人汇报上传结果
def wx_callback(content):
    wx_url = 'https://qyapi.weixin.qq.com/cgi-bin/webhook/send?key=8f4e9a5f-9ffc-46b0-82b5-f6d5fdca7d71'
    """艾特全部，并发送指定信息"""
    message = content + ' upload success'
    data = json.dumps({"msgtype": "text", "text": {"content": message, "mentioned_list": ["@all"]}})
    r = requests.post(wx_url, data, auth=('Content-Type', 'application/json'))


# 时间消耗
def print_cost_time(msg, begin_time):
	end_time = time.time()
	cost = "%.2f" % (end_time - begin_time)
	print(" %s cost:%s s" % (msg, cost))

# # 压缩功能
# def zip_files(dirPath, zipFilePath=None, includeDirInZip=True):
# 	start_time = time.time();
# 	if not zipFilePath:
# 		zipFilePath = dirPath + ".zip";
# 	if not os.path.isdir(dirPath):
# 		raise OSError("dirPath "+dirPath+" does not.");
# 	parentDir, dirToZip = os.path.split(dirPath)
# 	#Little nested function to prepare the proper archive path
# 	def trimPath(path):
# 		archivePath = path.replace(parentDir, "", 1)
# 		#if parentDir:
# 		#	archivePath = archivePath.replace(os.path.sep, "", 1)
# 		if not includeDirInZip:
# 			archivePath = archivePath.replace(dirToZip + os.path.sep, "", 1);
# 		return os.path.normcase(archivePath)
# 	outFile = zipfile.ZipFile(zipFilePath,"w",compression=zipfile.ZIP_DEFLATED,allowZip64=True)
# 	for(archiveDirPath,dirNames,fileNames) in os.walk(dirPath):
# 		for fileName in fileNames:
# 			filePath=os.path.join(archiveDirPath,fileName);
# 			outFile.write(filePath, trimPath(filePath));
#         #Make sure we get empty directories as well
#         if not fileNames and not dirNames:
#             zipInfo = zipfile.ZipInfo(trimPath(archiveDirPath) + "/")
#             #some web sites suggest doing
#             #zipInfo.external_attr = 16
#             #or
#             #zipInfo.external_attr = 48
#             #Here to allow for inserting an empty directory.  Still TBD/TODO.
#             outFile.writestr(zipInfo, "");
# 	outFile.close()
# 	print_cost_time("zip files", start_time)
#
# def tar_files(dirPath, zipFilePath):
# 	spath=os.path.split(dirPath)
# 	parentDirPath=spath[0]
# 	dirName=spath[1]
# 	start_time = time.time()
# 	os.system("tar -C %s -zcvf %s %s"
# 		%(parentDirPath,zipFilePath,dirName))
# 	print_cost_time("tar files", start_time)


# 定义上传类
class UploadFile2OSS():
    def __init__(self, objectname, file):
        self.objectname = objectname
        self.file = file
        self.ossBucket = self.initOSS()

    def initOSS(self):
        '''
        OSS初始化
        :return:
        '''
        access_key_id     = self.readConfigContent('common', 'access_id')
        access_key_secret = self.readConfigContent('common', 'secret_key')
        oss_endpoint      = self.readConfigContent('oss', 'endpoint')
        oss_bucket_name   = self.readConfigContent('oss', 'bucket_name')

        # OSS认证
        auth = oss2.Auth(access_key_id, access_key_secret)
        bucket = oss2.Bucket(auth, oss_endpoint, oss_bucket_name)
        return bucket

    def readConfigContent(self, contentid, keyValue):
        '''

        :param content: 配置文件中的一级字段
        :param keyValue: key字段
        :return:

        '''

        configFile = os.getcwd() + '/config.txt'
        print(configFile)
        cf = configparser.ConfigParser()
        cf.read(configFile)
        value = cf.get(contentid, keyValue)
        return value

    def percentage(self,consumed_bytes, total_bytes):
        if total_bytes:
            rate = int(100 * (float(consumed_bytes) / float(total_bytes)))
            print('\r{0}% '.format(rate), end=self.file)
            sys.stdout.flush()

    def uploadFile(self):
        try:
            oss2.resumable_upload(self.ossBucket, self.objectname, self.file,
                                  multipart_threshold=100 * 1024,
                                  num_threads=4,
                                  progress_callback=self.percentage)
        except Exception as e:
            print(e)



if __name__ == '__main__':
    # 脚本需要传入3个参数
    if (len(sys.argv) > 3):
        obejctName  = sys.argv[1]
        filePath    = sys.argv[2]
        projectName = sys.argv[3]
        # fileName = filePath.split("/")[-1]
    else:
        print("Example: %s  objectname  /data/backup.zip delta" % sys.argv[0])
        exit()

    uploader = UploadFile2OSS(obejctName, filePath)
    uploader.uploadFile()

    # 此处需要添加上传成功的判断
    wx_callback(projectName)







