from flask import Flask, render_template
import re


app = Flask(__name__)


STUDENT = {'name': 'wx', 'age': 18, 'gender': '女'}

STUDENT_LIST = [
    {'name': 'wx', 'age': 27, 'gender': '男'},
    {'name': 'xpd', 'age': 3, 'gender': '女'},
    {'name': 'cs', 'age': 23, 'gender': '女'}
]

STUDENT_DICT = {
    'A': {'name': 'wx', 'age': 27, 'gender': '男'},
    'B': {'name': 'xpd', 'age': 3, 'gender': '女'},
    'C': {'name': 'cs', 'age': 23, 'gender': '女'}
}


# 模版语法
@app.route('/test1')
def test1():

    return render_template('test1.html', **STUDENT)


@app.route('/test2')
def test2():

    return render_template('test2.html', student_list=STUDENT_LIST)


@app.route('/test3')
def test3():

    return render_template('test3.html', student_dict=STUDENT_DICT)


# 过滤器
@app.route('/filter')
def test_filter():

    return render_template('test4.html', student_list=STUDENT_LIST)


# 自定义过滤器
# 方式一：app.jinja_env.filters
def list_split(lst):
    return lst[:3]

app.jinja_env.filters['list_split'] = list_split


# 方式二：template_filter装饰器
@app.template_filter('get_even')
def get_even(lst):
    new_list = [item for item in lst if item%2==0]

    return new_list


# 测试器
@app.route('/test_test')
def test_test():

    return render_template('test5.html')


# 自定义测试器
# 先创建一个函数，然后将这个函数注册成测试器
# 方式一：app.jinja_env.tests
def test_phone(phone):
    pattern = r'1[3-9]\d{9}'
    return re.match(pattern, phone)  # 返回值一定是一个布尔值

app.jinja_env.tests['test_tel'] = test_phone

# 方式二：template_test装饰器
@app.template_test('start_with')
def start_with(my_str, suffix):
    return my_str.lower().startswith(suffix.lower())  # 返回值一定是一个布尔值



if __name__ == '__main__':
    
    app.run(debug=True, host='0.0.0.0', port=5000)
