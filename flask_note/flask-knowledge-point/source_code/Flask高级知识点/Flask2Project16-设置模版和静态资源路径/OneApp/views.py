from flask import Blueprint, render_template
from .models import *
from .exts import cache


blue = Blueprint('blue', __name__)


@blue.route('/')
def index():

    return render_template('index.html')
