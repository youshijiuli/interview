from flask import Flask, request
from flask import redirect, url_for, render_template
from db_instance import db
from flask_migrate import Migrate
from models import User

import uuid

class DefaultConfig(object):

    SECRET_KEY = str(uuid.uuid4())
    SQLALCHEMY_DATABASE_URI = 'sqlite:///sqlite3.db'
    SQLALCHEMY_TRACK_MODIFICATIONS = False


app = Flask(__name__)
app.config.from_object(DefaultConfig)

migrate = Migrate()


db.init_app(app)
migrate.init_app(app=app, db=db)


@app.route('/')
def index():

    return "hello"


@app.route('/add_user', methods=['GET', 'POST'])
def add_user():

    if request.method == 'GET':

        return render_template('register.html')
    elif request.method == 'POST':
        
        username = request.form.get('username')

        new_user = User(username=username, gender=True)
        db.session.add(new_user)
        db.session.commit()

        return "添加成功！"

    else:
        return render_template('register.html')



@app.route('/delete_user')
def delete_user():
    # 删掉最后一个
    last_user = User.query.order_by(User.id.desc()).first()
    db.session.delete(last_user)
    db.session.commit()  # 记得提交
    return "删掉最后一个用户成功！"


@app.route('/update_user')
def update_user():
    # 修改所有用户性别
    all_user = User.query.all()
    for user in all_user:
        user.gender = not user.gender

    db.session.commit()  # 操作完后记得提交操作

    return "修改所有用户性别成功！"


@app.route('/search_user')
def search_user():

    username = request.args.get('username')

    user = User.query.filter(User.username==username).first()

    if user:
        return f"用户名：{user.username} \t 性别:{user.gender}"
    else:
        return f"没找到{username}用户"


if __name__ == '__main__':
    
    app.run(debug=False, host='0.0.0.0', port=5000)

