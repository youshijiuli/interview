import requests

url_list = [
    'https://www3.autoimg.cn/newsdfs/g26/M02/35/A9/120x90_0_autohomecar__ChsEe12AXQ6AOOH_AAFocMs8nzU621.jpg',
    'https://www2.autoimg.cn/newsdfs/g30/M01/3C/E2/120x90_0_autohomecar__ChcCSV2BBICAUntfAADjJFd6800429.jpg',
    'https://www3.autoimg.cn/newsdfs/g26/M0B/3C/65/120x90_0_autohomecar__ChcCP12BFCmAIO83AAGq7vK0sGY193.jpg'
]

"""
# python伪造浏览器向地址发送请求
	rep = requests.get(url)

	# 请求返回回来的字节
	# print(rep.content)

	with open('xxxxxx.jpg',mode='wb') as f:
		f.write(rep.content)
"""

for url in url_list:
    ret = requests.get(url)
    filename = url.rsplit('/', maxsplit=1)[-1]
    with open(f'images/{filename}', 'wb') as f:
        # 小文件
        # f.write(ret.content)

        # 大文件
        for chunk in ret.iter_content():
            f.write(chunk)
        print(f'{filename}下载完毕')
