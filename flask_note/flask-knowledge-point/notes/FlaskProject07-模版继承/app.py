from flask import Flask
from flask import render_template



app = Flask(__name__)


@app.route('/')
def index():

    return render_template('base.html')


@app.route('/child1')
def child1():

    return render_template('child1.html')


@app.route('/child2')
def child2():

    return render_template('child2.html')

if __name__ == '__main__':
    
    app.run(debug=True, host='0.0.0.0', port=5000)
