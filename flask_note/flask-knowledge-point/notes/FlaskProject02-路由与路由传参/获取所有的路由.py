from flask import Flask, json


app = Flask(__name__)


@app.route('/')
def index():
    # Flask的app有一个url_map属性，是一个Map对象类似列表
    # 里面有所有的视图和路由信息
    """
    Map([<Rule '/static/<filename>' (OPTIONS, HEAD, GET) -> static>,
 <Rule '/' (OPTIONS, HEAD, GET) -> index>])
    """
    print(app.url_map)

    # 可以使用url_map的iter_rules()方法来得到一个迭代器
    rules = app.url_map.iter_rules()
    print(rules, type(rules))  # <list_iterator object at 0x0000020DC2FFB2E0> <class 'list_iterator'>
    return 'hello'


@app.route('/test1')
def test1():
    # 查看一下迭代器里面是什么样子的
    rules = app.url_map.iter_rules()

    for rule in rules:
        print(f"name={rule.endpoint}  path={rule.rule}")

    return 'hello'


@app.route('/test2')
def test2():
    # 得到迭代器
    rules = app.url_map.iter_rules()
    # 使用flask自带的json模块可以构造json类型的响应
    return json.dumps(
            {rule.endpoint: rule.rule for rule in rules}
        )


if __name__ == '__main__':

    app.run()
