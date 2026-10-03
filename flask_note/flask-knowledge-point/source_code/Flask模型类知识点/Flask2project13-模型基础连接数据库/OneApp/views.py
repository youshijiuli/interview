from flask import Blueprint, render_template
from .models import *


blue = Blueprint('blue', __name__)


@blue.route('/')
def index():

    context = {
        'hello': 'hello flask!'
    }

    return render_template('index.html', **context)



