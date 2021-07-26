import cv2
import numpy as np
from PIL import Image
def prepare_test_image(image_path, resize_shape = (256,256), color_mode = "gray"):
    resized_image = cv2.resize(cv2.imread(image_path),resize_shape)
    resized_image = resized_image/255.
    if color_mode == "gray":
        img_array = resized_image[:,:,0]
    elif color_mode == "rgb":
        img_array = resized_image[:,:,:]
    img_array = np.array(img_array).reshape(1,256,256,1)
    return img_array
### U-net 

from keras.models import *
from keras.layers import *
from keras.optimizers import *
from keras import backend as keras
from keras.preprocessing.image import ImageDataGenerator
from keras.callbacks import ModelCheckpoint, LearningRateScheduler
from tensorflow.keras.activations import *
def unet(input_size=(256,256,1)):
    inputs = Input(input_size)
    
    conv1 = Conv2D(32, (3, 3), activation='relu', padding='same')(inputs)
    conv1 = Conv2D(32, (3, 3), activation='relu', padding='same')(conv1)
    
    pool1 = MaxPooling2D(pool_size=(2, 2))(conv1)

    conv2 = Conv2D(64, (3, 3), activation='relu', padding='same')(pool1)
    conv2 = Conv2D(64, (3, 3), activation='relu', padding='same')(conv2)
    
    pool2 = MaxPooling2D(pool_size=(2, 2))(conv2)

    conv3 = Conv2D(128, (3, 3), activation='relu', padding='same')(pool2)
    conv3 = Conv2D(128, (3, 3), activation='relu', padding='same')(conv3)
   
    pool3 = MaxPooling2D(pool_size=(2, 2))(conv3)

    conv4 = Conv2D(256, (3, 3), activation='relu', padding='same')(pool3)
    conv4 = Conv2D(256, (3, 3), activation='relu', padding='same')(conv4)
    
    pool4 = MaxPooling2D(pool_size=(2, 2))(conv4)

    conv5 = Conv2D(512, (3, 3), activation='relu', padding='same')(pool4)
    conv5 = Conv2D(512, (3, 3), activation='relu', padding='same')(conv5)

    up6 = concatenate([Conv2DTranspose(256, (2, 2), strides=(2, 2), padding='same')(conv5), conv4], axis=3)
    conv6 = Conv2D(256, (3, 3), activation='relu', padding='same')(up6)
    conv6 = Conv2D(256, (3, 3), activation='relu', padding='same')(conv6)

    up7 = concatenate([Conv2DTranspose(128, (2, 2), strides=(2, 2), padding='same')(conv6), conv3], axis=3)
    conv7 = Conv2D(128, (3, 3), activation='relu', padding='same')(up7)
    conv7 = Conv2D(128, (3, 3), activation='relu', padding='same')(conv7)

    up8 = concatenate([Conv2DTranspose(64, (2, 2), strides=(2, 2), padding='same')(conv7), conv2], axis=3)
    conv8 = Conv2D(64, (3, 3), activation='relu', padding='same')(up8)
    conv8 = Conv2D(64, (3, 3), activation='relu', padding='same')(conv8)

    up9 = concatenate([Conv2DTranspose(32, (2, 2), strides=(2, 2), padding='same')(conv8), conv1], axis=3)
    conv9 = Conv2D(32, (3, 3), activation='relu', padding='same')(up9)
    conv9 = Conv2D(32, (3, 3), activation='relu', padding='same')(conv9)

    conv10 = Conv2D(1, (1, 1), activation='sigmoid')(conv9)

    return Model(inputs=[inputs], outputs=[conv10])
    # /home/vanhocvp/Code/DIP/Demo/app/AI/checkpoint-20210610T172837Z-001
checkpoint_path = './app/AI/checkpoint-20210610T172837Z-001/checkpoint/cp1.ckpt'
model = unet(input_size=(256,256,1))
model.load_weights(checkpoint_path)
import cv2
from datetime import datetime
def predict(img_path, name):
    image = prepare_test_image(img_path)
    pred = model.predict(image)
    pred[pred>0.5] = 1.0
    pred[pred<0.5] = 0.0
    pred = np.reshape(pred, (256,256))
    pred *= 255
    img_new = Image.fromarray(pred)
    img_new = img_new.convert('L')

    t = datetime.now()
    file_name =  f"/static/images/dip/{name}_{t.hour}_{t.minute}_{t.second}.png"
    img_new.save("./app"+file_name)
    return file_name