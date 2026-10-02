import configparser

config = configparser.ConfigParser()
config.read('config.ini')  # 替换为您的 ini 文件路径

print(config.sections())  # 打印所有节
# ['Section1', 'Section2', 'Connection']


# 读取特定节和选项的值
# section_name = 'Section1'
# option_name = 'key1'
#
# value = config.get(section_name, option_name)
# print(f"{option_name} 的值为: {value}")


# section_name = 'Connection'
# print(config.get(section_name, 'host'))
# print(config.get(section_name, 'port'))


