#!/usr/bin/env python

import cv2
import numpy as np
import os
import random
from tqdm import tqdm


def main():
    BLACK = [0,0,0]
    #Read the files
    for filename in tqdm(os.listdir('../../data/4000unlabeledLP')):
        img = cv2.imread('../../data/4000unlabeledLP/'+filename)

        img = cv2.cvtColor(img, cv2.COLOR_RGBA2RGB)
        height = img.shape[0]
        width = img.shape[1]
        # Calculate how much padding is needed for the width
        padding_x = (max_width - width) // 2
        # Calculate how much padding is needed for the height
        padding_y = (max_height - height) // 2

        img = cv2.copyMakeBorder(img,padding_y,padding_y,padding_x,padding_x,cv2.BORDER_CONSTANT,value=BLACK)
        cv2.imwrite('../../data/4000unlabeledLP_padded/'+filename,img)
    #Read the blurred files
    for filename in tqdm(os.listdir('../../data/4000unlabeledLP_blurred')):
        img = cv2.imread('../../data/4000unlabeledLP_blurred/'+filename)
        img = cv2.cvtColor(img, cv2.COLOR_RGBA2RGB)
        height = img.shape[0]
        width = img.shape[1]
        # Calculate how much padding is needed for the width
        padding_x = (max_width - width) // 2
        # Calculate how much padding is needed for the height
        padding_y = (max_height - height) // 2

        img = cv2.copyMakeBorder(img,padding_y,padding_y,padding_x,padding_x,cv2.BORDER_CONSTANT,value=BLACK)
        cv2.imwrite('../../data/4000unlabeledLP_blurred_padded/'+filename,img)

if __name__ == '__main__':
    main()
