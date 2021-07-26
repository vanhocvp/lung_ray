from flask.helpers import url_for
from . import *
from .models import *
from flask import request, render_template, session
import requests, json, os
from PIL import Image
import io
from io import StringIO
from urllib.request import urlopen
from werkzeug.utils import redirect, secure_filename
import cv2
import numpy as np
from datetime import datetime
import ast
t = datetime.now()
PATH_RAW = f"/static/images/dip/test1_{t.hour}_{t.minute}_{t.second}.png"
@main.route('/dip', methods = ['GET', 'POST'])
def dip():
    if request.method == 'POST':
        URL = request.form['homepage']
        if URL != '':
            filename = secure_filename(URL.rpartition('/')[-1])
            file = io.BytesIO(urlopen(URL).read())
            img = Image.open(file)
            t = datetime.now()
            PATH_RAW = f"/static/images/dip/test1_{t.hour}_{t.minute}_{t.second}.png"
            img.save('./app'+PATH_RAW)
            image = cv2.imread('./app'+PATH_RAW)
            PATH_RAW = f"/static/images/dip/test1_{t.hour}_{t.minute}_{t.second}.png"
            image = cv2.resize(image, (256,256))
            image = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
            cv2.imwrite('./app'+PATH_RAW, image)
            session['path_img_1'] = PATH_RAW
            return redirect(url_for('main.process'))
        elif 'file1' in request.files and request.files['file1'].filename != '':
            file1 = request.files['file1']
            t = datetime.now()
            PATH_RAW = f"/static/images/dip/test1_{t.hour}_{t.minute}_{t.second}.png"
            file1.save('./app'+PATH_RAW)
            image = cv2.imread('./app'+PATH_RAW)
            print (image)
            PATH_RAW = f"/static/images/dip/test1_{t.hour}_{t.minute}_{t.second}.png"
            image = cv2.resize(image, (256,256))
            image = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
            cv2.imwrite('./app'+PATH_RAW, image)
            session['path_img_1'] = PATH_RAW
            return redirect(url_for('main.process'))
    return '''
    <h1>Upload new File</h1>
    <form method = "post" enctype="multipart/form-data">
        <label for="homepage">Url:</label>
        <input type="url" id="homepage" name="homepage">
        <label for="homepage">or</label>
        <input type="file" name="file1">
        <br><br>
        <input type="submit">
    </form>
    '''
@main.route('/predict', methods = ["POST"])
def index():
    arg = request.get_data()
    arg = arg.decode("utf-8") 
    if arg == "btn_1":
        path_img = session['path_img_1']
        name = 'img_1'
        mask, segment = predict(path_img, name)
        session['path_mask_1'] = mask
        session['path_segment_1'] = segment
    elif arg == "btn_2":
        path_img = session['path_img_2']
        name = 'img_2'
        mask, segment = predict(path_img, name)
        session['path_mask_2'] = mask
        session['path_segment_2'] = segment
    elif arg == "btn_3":
        path_img = session['path_img_3']
        name = 'img_3'
        mask, segment = predict(path_img, name)
        session['path_mask_3'] = mask
        session['path_segment_3'] = segment
    return 'predict_done'
@main.route("/dip/process", methods = ['GET', 'POST'])
def process():
    PATH_RAW = session['path_img_1']
    um_input = request.form.get('slider_1')
    hef_input = request.form.get('slider_2')
    btn = request.form.get('btn_1')
    tag_first = um_input
    if um_input is None:
        um_input = 5
    if hef_input is None:
        hef_input = 50
    if tag_first is not None:
        if um_input != session['slider_1']:
            session['slider_1'] = um_input
            filter = request.form.get('checkbox')
            print (filter, um_input)
            file_name_2 = UM_DIP(PATH_RAW, int(filter), int(um_input))
            session['path_img_2']  = file_name_2
        if hef_input != session['slider_2']:
            session['slider_2'] = hef_input
            file_name_3 = HEF_DIP(PATH_RAW, int(hef_input))
            session['path_img_3']  = file_name_3
            
    else:
        session['slider_1'] = um_input
        session['slider_2'] = hef_input
        file_name_2 = UM_DIP(PATH_RAW, 3, int(um_input))
        file_name_3 = HEF_DIP(PATH_RAW, int(hef_input))
        session['path_img_2']  = file_name_2
        session['path_img_3']  = file_name_3
        print (session)
    print("Done process image")
    return render_template("upload.html")


@main.after_request
def add_header(response):
    """
    Add headers to both force latest IE rendering engine or Chrome Frame,
    and also to cache the rendered page for 10 minutes.
    """
    response.headers['X-UA-Compatible'] = 'IE=Edge,chrome=1'
    response.headers['Cache-Control'] = 'no-store, max-age=0'
    return response
