from __future__ import division, print_function, absolute_import

import tflearn
from tflearn.layers.core import input_data
from tflearn.layers.conv import conv_2d, conv_2d_transpose, max_pool_2d
from tflearn.layers.estimator import regression
import glob
import numpy as np
import cv2
from tqdm import tqdm
import os

TRAINING_PATH_Y = '../data/4000unlabeledLP_padded/'
TRAINING_PATH_X = '../data/4000unlabeledLP_blurred_padded/'
IMG_HEIGHT = 78
IMG_WIDTH = 245
LR = 1e-3
MODEL_NAME = 'deblurring-{}-{}.model'.format(LR, '1')


class NeuralNet():
    def __init__(self):
        self.model = self.__create_model()
        if os.path.exists('models/{}.meta'.format(MODEL_NAME)):
            model.load(MODEL_NAME)

    def __create_model(self):
        # Building convolutional network
        network = input_data(shape=[None, IMG_HEIGHT, IMG_WIDTH, 3], name='input')
        network = conv_2d_transpose(network, 64, 9, [IMG_HEIGHT*2, IMG_WIDTH*2, 64], strides=2,  activation='relu', regularizer="L2")
        network = max_pool_2d(network, 2)
        network = conv_2d_transpose(network, 128, 3, [IMG_HEIGHT*2, IMG_WIDTH*2, 128], strides=2,  activation='relu', regularizer="L2")
        network = max_pool_2d(network, 2)
        network = conv_2d(network, 128, 9, activation='LeakyReLU', regularizer="L2")
        network = conv_2d(network, 64, 7, activation='LeakyReLU', regularizer="L2")
        network = conv_2d(network, 3, 3, activation='LeakyReLU', regularizer="L2")
        network = regression(network, optimizer='adam', learning_rate=0.01,
                             loss='categorical_crossentropy', name='target')
        model = tflearn.DNN(network, tensorboard_verbose=0)
        return model

    def predict(self, img):
        data = cv2.resize(img,(IMG_WIDTH,IMG_HEIGHT))
        data = cv2.cvtColor(data, cv2.COLOR_RGBA2RGB)
        data = data.reshape(-1,IMG_HEIGHT,IMG_WIDTH,3)
        output = self.model.predict(data)[0]
        return output

    def train(self):
        if os.path.isfile('train_data_X.npy') is False:
            process_test_data(TRAINING_PATH_X,'X')
        train_data_X = np.load('train_data_X.npy')
        if os.path.isfile('train_data_Y.npy') is False:
            process_test_data(TRAINING_PATH_Y,'Y')
        train_data_Y = np.load('train_data_Y.npy')
        X = np.array([i for i in train_data_X]).reshape(-1, IMG_HEIGHT, IMG_WIDTH, 3)
        Y = np.array([i for i in train_data_Y]).reshape(-1, IMG_HEIGHT, IMG_WIDTH, 3)
        if os.path.exists('models/{}.meta'.format(MODEL_NAME)) is False:
            self.model.save('models/{}.model'.format(MODEL_NAME))
        self.model.fit({'input': X}, {'target': Y}, n_epoch=3,
               snapshot_step=100, show_metric=True, run_id=MODEL_NAME)


# Data loading and preprocessing
def process_test_data(filepath,value):
    test_data = []
    for img in tqdm(os.listdir(filepath)):
        path = os.path.join(filepath,img)
        img = cv2.resize(cv2.imread(path),(IMG_HEIGHT,IMG_WIDTH))
        img = cv2.cvtColor(img, cv2.COLOR_RGBA2RGB)
        test_data.append(np.array(img))
    np.save('train_data_'+value+'.npy',test_data)
    return test_data

def main():
    model = NeuralNet()
    model.train()


if __name__ == '__main__':
    main()
