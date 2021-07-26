from .dip.src.algorithms.hef import HEF
from .dip.src.algorithms.unsharping_mask import UM
from .AI import segment as predict_segment
import os
import imageio
from flask import session
from datetime import datetime
import cv2
def HEF_DIP(path, d0v):
    hef_alg = HEF(path, d0v)
    image = hef_alg.run()
    t = datetime.now()
    name = 'test3'  
    try:
        old_file = session['path_img_3']
        os.remove('./app'+old_file)
    except:
        pass
    file_name =  f"/static/images/dip/{name}_{t.hour}_{t.minute}_{t.second}.png"
    imageio.imwrite("./app"+file_name, image)
    return file_name
def UM_DIP(path, filter, amount):
    um_alg = UM(path, filter, amount)
    image = um_alg.run()
    t = datetime.now()
    name = 'test2'
    try:
        old_file = session['path_img_2']
        os.remove('./app'+old_file)
    except:
        pass
    file_name =  f"/static/images/dip/{name}_{t.hour}_{t.minute}_{t.second}.png"
    imageio.imwrite("./app"+file_name, image)
    return file_name
def predict(path_img, name):
    PATH_DIR = "./app"
    file_name_mask = predict_segment.predict(PATH_DIR+path_img, name)
    raw = cv2.imread(PATH_DIR+path_img)
    raw = cv2.resize(raw, (256,256))
    mask = cv2.imread(PATH_DIR+file_name_mask, cv2.COLOR_BGR2GRAY)
    segment = cv2.bitwise_and(raw, raw, mask = mask)
    t = datetime.now()
    name_segment = name+'_segment'
    file_name_segment =  f"/static/images/dip/{name_segment}_{t.hour}_{t.minute}_{t.second}.png"
    imageio.imwrite("./app"+file_name_segment, segment)
    return file_name_mask, file_name_segment