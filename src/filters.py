import numpy as np
import cv2

def laplacian(img):
    kernel = np.array([[-1,-1,-1], [-1,9,-1], [-1,-1,-1]])
    return cv2.filter2D(img, -1, kernel)

def median(img):
    img =cv2.medianBlur(img,3)
    return cv2.medianBlur(img,3)

def bilateral(img):
    return cv2.bilateralFilter(img,15,5,5)
