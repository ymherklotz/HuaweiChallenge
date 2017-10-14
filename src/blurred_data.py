import cv2
import numpy as np
import os
import random
from tqdm import tqdm


def main():
    #Read the file
    for filename in tqdm(os.listdir('../data/4000unlabeledLP')):
        img = cv2.imread('../data/4000unlabeledLP/'+filename)
        img = cv2.cvtColor(img, cv2.COLOR_RGBA2RGB)

        #Create a random sized kernel from 3 - 11
        kernel = random.randrange(3,12,2)
        #Random type of the blur
        blur = random.randrange(0,3)

        #Averate blur
        if blur == 0:
            dst = cv2.blur(img,(kernel,kernel))
        #Gaussian Blur
        if blur == 1:
            dst = cv2.GaussianBlur(img,(kernel,kernel),0)
        #Median Blur
        if blur == 2:
            dst = cv2.medianBlur(img,kernel)
        #Save the image
        cv2.imwrite('../data/4000unlabeledLP_blurred/'+filename,dst)

if __name__ == '__main__':
    main()
