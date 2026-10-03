from flask import Flask
from flask import render_template, request, make_response


app = Flask(__name__)


@app.route('/')
def index():
    uid = request.cookies.get('uid')
    name = request.cookies.get('name')
    return render_template('index.html', uid=uid, name=name)


@app.route('/login/<int:uid>')
def login(uid):
    name = request.args.get('name')
    print(uid, name)
    
  
    return render_template('index.html', uid=uid, name=name)


if __name__ == '__main__':
    
    app.run(debug=True, host="0.0.0.0", port=5000)
