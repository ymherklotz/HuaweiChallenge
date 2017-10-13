import cv2
import numpy as np
import os
from matplotlib import pyplot as plt


def main():
    for filename in os.listdir('../data/4000unlabeledLP'):
        img = cv2.imread('../data/4000unlabeledLP/'+filename)
        img = cv2.cvtColor(img, cv2.COLOR_RGBA2RGB)
        dst = cv2.fastNlMeansDenoisingColored(img,None,10,10,7,21)
        plt.subplot(121),plt.imshow(img)
        plt.subplot(122),plt.imshow(dst)
        plt.show()
        break

if __name__ == '__main__':
    main()
