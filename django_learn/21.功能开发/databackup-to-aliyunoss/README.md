#  项目简介

**databackup-to-aliyunoss 是一个本地数据上传到阿里OSS的Python脚本。**

**主要作用是：各个事业部下各项目组的Mysql、MongoDB备份数据分别使用此脚本上传到阿里OSS对应的bucket下的对应文件夹下。**

# 项目文件解读

- aliyun-oss-upload.py ：这个是上传数据所需脚本，直接使用即可，不需要改动。
- config.txt ：这个是需要改动的文件，有阿里的AK/SK、OSS的endpoint、bucket名称
```shell
[common]
# access_id
access_id = xxxxxxxxxxxxxxxxxxx   # AK/SK 需要修改，需要企业微信运维工单申请

# secret_key
secret_key = xxxxxxxxxxxxxxxxxxx

[oss]
# OSS endpoint
endpoint = oss-cn-beijing-internal.aliyuncs.com   
# endpoint不用修改，但使用的服务器必须也在华北2区，否则需要使用公网endpoint，会产生额外的流量费用


# OSS bucketname
bucket_name = test   
# 修改成你需要上传到的bucket名称，每个事业部不同，请查看本项目图片文件确认
```

# 命令结构

```shell
python3 aliyun-oss-upload.py 阿里oss路径 本地文件路径 企业微信机器人提醒
```

# 使用教程

## 运行环境

- Python3+ 
- Python模块：oss2、requests、configparser、json



##  环境准备

1. 安装Python3.7环境 （安装步骤不再详细介绍，具体请查看官网https://www.python.org)
2. 安装脚本所需模块

```shell
pip3 install oss2 requests configparser json
```

3. 查看本文档中的**阿里OSS bucket名称及目录名称**，确认你需要上传到的bucket名称及文件夹名称。



## 使用示例

```shell
python3 aliyun-oss-upload.py test/mongo/apache-jmeter-5.1.1.tgz /root/apache-jmeter-5.1.1.tgz delta
```

**参数解析：**

- Python3：本项目需要使用Python3以上版本，示例使用的为Python3.7
- aliyun-oss-upload.py ：数据上传脚本文件
- deltatest/mongo/apache-jmeter-5.1.1.tgz ：因为bucket名称在config.txt文件中确定了，所以这里只需要写bucket下的目录路径
- /root/apache-jmeter-5.1.1.tgz ：需要上传的文件路径
- delta ：企业微信机器人通知消息，上传成功会发消息提醒，请写你的项目组名称

![JbBIdU.png](https://s1.ax1x.com/2020/04/30/JbBIdU.png)

# 阿里OSS bucket名称及目录名称

**阿里OSS bucket名称及目录名称的命名**根据事业部及项目组来命名，如下图：

![JqnKUO.png](https://s1.ax1x.com/2020/04/30/JqnKUO.png)

**相对应的bucket名称和目录名称，如下图：**

![Jq1xW8.png](https://s1.ax1x.com/2020/04/30/Jq1xW8.png)

# 子账号授权

**各个事业部分别使用不同的子账号，授权对应的bucket只上传权限**

```json
{
    "Version": "1",
    "Statement": [
        {
            "Effect": "Allow",
            "Action": [
                "oss:Put*"
            ],
            "Resource": [
                "acs:oss:*:*:bucket名称/*"
            ],
            "Condition": {}
        }
    ]
}
```