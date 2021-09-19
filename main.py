import os
from flask import Flask, flash, url_for, request, render_template
from werkzeug.utils import redirect, secure_filename
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
import seaborn as sns


os.environ['TF_CPP_MIN_LOG_LEVEL'] = '3'

app = Flask(__name__)
UPLOAD_FOLDER = './static/gambar/'

@app.route('/')
def index():
    return "hello"

@app.route('/bi_piechart')
def bi_piechart():
    return render_template('home.html', lahan=lahan)