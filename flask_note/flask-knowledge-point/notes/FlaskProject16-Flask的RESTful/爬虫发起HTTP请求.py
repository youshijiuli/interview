import requests


def spider():
    """ 用爬虫来请求API接口 """
    url = 'http://127.0.0.1:5000/hello'
    method = input('HTTP method：')

    if method == 'get':
        # get:查询
        resp = requests.get(url=url)
    elif method == 'post':
        # post:新增
        resp = requests.post(url=url)
    elif method == 'put':
        # put:修改
        resp = requests.put(url=url)
    elif method == 'delete':    
        # delete:删除
        resp = requests.delete(url=url)
    else:
        return None

    return resp.text


if __name__ == '__main__':
    
    while True:
        result = spider()
        print(result)
        if not result:
            break
