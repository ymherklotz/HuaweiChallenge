import argparse
import cv2
from network import NeuralNet
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
    ax1 = fig.add_subplot(2,2,1)
    ax1.imshow(img)

    #Stage 1 add padding
    img,y,x = add_padding(img)

    #Stage 2 openCV optimization

    #Stage 3 Machine Learning Deblur
    model = NeuralNet()
    img = model.predict(img)

    #Stage 4 More openCV

    #End
    ax2 = fig.add_subplot(2,2,2)
    img = remove_padding(img,x,y)
    ax2.imshow(img)
    plt.show()


if __name__ == '__main__':
    main()
