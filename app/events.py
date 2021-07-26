from flask import session
from flask_socketio import emit, join_room, leave_room
from . import socketio
import requests, json



@socketio.on('raw_img', namespace='/dip/process')
def raw_img():
    path = session['path_img_1']
    print (path)
    emit('raw_img', {'path':path})
@socketio.on('slider_1', namespace='/dip/process')
def slider_1():
    path = session['path_img_2']
    print (path)
    emit('slider_1', {'path':path})
@socketio.on('slider_2', namespace='/dip/process')
def slider_2():
    path = session['path_img_3']
    print (path)
    emit('slider_2', {'path':path})
@socketio.on('predict_1', namespace='/dip/process')
def predict_1():
    path_mask = session['path_mask_1']
    path_segment = session['path_segment_1']
    emit('predict_1', {'path_mask':path_mask, 'path_segment':path_segment})
@socketio.on('predict_2', namespace='/dip/process')
def predict_2():
    path_mask = session['path_mask_2']
    path_segment = session['path_segment_2']
    emit('predict_2', {'path_mask':path_mask, 'path_segment':path_segment})
@socketio.on('predict_3', namespace='/dip/process')
def predict_3():
    path_mask = session['path_mask_3']
    path_segment = session['path_segment_3']
    emit('predict_3', {'path_mask':path_mask, 'path_segment':path_segment})
