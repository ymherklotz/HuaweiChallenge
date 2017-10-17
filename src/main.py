import argparse
import cv2
from network import NeuralNet
from filters import laplacian
from filters import median
from filters import bilateral
import matplotlib.pyplot as plt
import numpy as np

#This function is adding padding to the original image
#Stage 1
def add_padding(img):
    BLACK = [0,0,0]
    img = cv2.cvtColor(img, cv2.COLOR_RGBA2RGB)
    height = img.shape[0]
    width = img.shape[1]
    # Calculate how much padding is needed for the width
    padding_x = (245 - width) // 2
    # Calculate how much padding is needed for the height
    padding_y = (78 - height) // 2
    img = cv2.copyMakeBorder(img,padding_y,padding_y,padding_x,padding_x,cv2.BORDER_CONSTANT,value=BLACK)
    return (img,padding_x,padding_y)

def remove_padding(img, x, y):
    return img[x:img.shape[0]-x,y:img.shape[1]-y].copy()

def main():
    parser = argparse.ArgumentParser(description='Deblur image')
    parser.add_argument('-d','--data', help='Input data image')
    parser.add_argument('-o','--output', help='Output image')

    #START: Stage 0 load the image
    args = parser.parse_args()
    input_name = args.data
    img = cv2.imread(input_name)
    fig = plt.figure()
    ax1 = fig.add_subplot(3,3,1)
    ax1.set_title("Input image")
    ax1.imshow(img)

    #Stage 1 High pass filtering
    img = bilateral(img)
    ax2 = fig.add_subplot(3,3,2)
    ax2.set_title("Bilateral filtering")
    ax2.imshow(img)

    #Stage 2 Median filter
    img = median(img)
    ax3 = fig.add_subplot(3,3,3)
    ax3.set_title("Median filtering")
    ax3.imshow(img)

    #Stage 3 High pass filtering
    img = laplacian(img)
    ax4 = fig.add_subplot(3,3,4)
    ax4.set_title("High pass filtering")
    ax4.imshow(img)

    #Stage 1 add padding
    img,y,x = add_padding(img)

    #Stage 2 openCV optimization

    #Stage 3 Machine Learning Deblur
    model = NeuralNet()
    img = model.predict(img)

    #Stage 4 More openCV

    #End
    img = remove_padding(img,x,y)
    ax5 = fig.add_subplot(3,3,5)
    ax5.set_title("After machine learning")
    ax5.imshow(img)
    plt.show()


if __name__ == '__main__':
    main()
