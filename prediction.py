import threading
import numpy as np
import scipy.fftpack
from scipy.signal import stft,medfilt,firwin,convolve,butter,filtfilt
from scipy.signal import get_window
from scipy import interpolate
import pickle
from util_func import *
from qt import *
import itertools
import time
import keras
from tensorflow.keras.models import model_from_json

import tensorflow as tf
import numpy as np
from keras import backend as K

def recall_m(y_true, y_pred):
    true_positives = K.sum(K.round(K.clip(y_true * y_pred, 0, 1)))
    possible_positives = K.sum(K.round(K.clip(y_true, 0, 1)))
    recall = true_positives / (possible_positives + K.epsilon())
    return recall

def precision_m(y_true, y_pred):
    true_positives = K.sum(K.round(K.clip(y_true * y_pred, 0, 1)))
    predicted_positives = K.sum(K.round(K.clip(y_pred, 0, 1)))
    precision = true_positives / (predicted_positives + K.epsilon())
    return precision

def f1_m(y_true, y_pred):
    precision = precision_m(y_true, y_pred)
    recall = recall_m(y_true, y_pred)
    return 2*((precision*recall)/(precision+recall+K.epsilon()))

def resize_data(data, freq=50):
    x = np.linspace(0, len(data) - 1, num=len(data))
    t = (data[-1, 0] - data[0, 0]) / 1000000000
    f_list = [interpolate.interp1d(x, a, kind='quadratic') for a in data.T[1:]]
    x_new = np.linspace(0, len(data) - 1, num=int(t * freq))
    new_data = [f(x_new) for f in f_list]
    new_data = np.array(new_data).T
    return new_data[-128:]

def rotate_data(data_g, act_g=[0, -1, 0], gravity=None):
    data = np.copy(data_g)
    data = np.hstack((data, data[:, :3]))
    act_g = act_g
    if gravity is None:
        gravity = butter_lowpass_filter(data.T[:3], 0.1, 50, 1)
    else:
        gravity = gravity.T
    bodyData = data.T[:3] - gravity
    data[:, :3] = bodyData.T
    for i, row in enumerate(data):
        quat = acc_to_quat(bodyData.T[i], row[:3], act_g, g=gravity.T[i])
        data[i][:3] = rotate_vector(quat, row[:3])
        data[i][3:6] = rotate_vector(quat, row[3:6])
        data[i][-3:] = rotate_vector(quat, row[-3:])
    return data


class pred:

    def __init__(self):
        #threading.Thread.__init__(self)
        self.min_time = 3
        #self.limit  = 128
        self.conv_model = None
        #self.predict_every = 1
        with open('G:/Project Server Pred/Models/JSON_models/model_1.json', 'r') as json_file:
            json_model = json_file.read()
        self.conv_model = model_from_json(json_model)
        self.conv_model.load_weights("G:\Project Server Pred\model_weights\weights-model_non_rotated_1.h5")
        self.activities = ["WALKING","ASCEND","DESCEND","SITTING","STANDING","LYING"]


    """def process_data(self,data):
        acc_data = data['acc']
        gyro_data = data['gyro']
        if len(acc_data) == self.server.limit and len(gyro_data) == self.server.limit:
            acc_data = np.array(acc_data)
            gyro_data = np.array(gyro_data)
            acc_data = resize_data(acc_data)
            gyro_data = resize_data(gyro_data)
            total_data = np.hstack((acc_data, gyro_data))
            return total_data
        else:
            return None"""

    def process_data(self,data):
        acc_data = data['acc']
        gyro_data = data['gyro']
        if len(acc_data)==0 or len(gyro_data)==0:
            return None
        elif (acc_data[-1][0] - acc_data[0][0])/1000000000 >= self.min_time and (gyro_data[-1][0] - gyro_data[0][0])/1000000000 >= self.min_time:
            acc_data = np.array(acc_data)
            gyro_data = np.array(gyro_data)
            acc_data = resize_data(acc_data)
            gyro_data = resize_data(gyro_data)
            total_data = np.hstack((acc_data, gyro_data))
            return total_data
        else:
            return None


    def predict(self,data):

        p_data = self.process_data(data)
        if p_data is not None:
            processed_data = p_data.copy()
            final_data = rotate_data(processed_data)
            final_data = final_data[:, :6]
            final_data = final_data.reshape((1, final_data.shape[0], final_data.shape[1]))

            prediction = self.conv_model.predict(final_data)[0]

            print("predicted: ", self.activities[np.argmax(prediction)])
            return prediction

            #start_time = time.time()
        else:
            return None
            #pass
            #print("Waiting for prediction")

    """def run(self):
        start_time = time.time()
        while (True):

            if time.time() - start_time> self.predict_every:
                data = self.server.return_value()
                p_data = self.process_data(data)
                if p_data is not None:
                    processed_data = p_data.copy()
                    final_data = rotate_data(processed_data)
                    final_data = final_data[:, :6]
                    final_data = final_data.reshape((1, final_data.shape[0], final_data.shape[1]))

                    prediction = np.argmax(self.conv_model.predict(final_data)[0])
                    print("predicted: ", self.activity_list[prediction])
                    start_time = time.time()
                else:
                    pass
                    print("Waiting for prediction")"""

