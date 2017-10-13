import cv2
import numpy as np
import os
import glob

if __name__ == '__main__':
    main()


def main():
    image_list = glob.glob('data/4000unlabeledLP/*.jpg')
    x = np.array([np.array(Image.open(fname)) for img in image_list])
