import argparse
import cv2

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
    img = cv2.copyMakeBorder(img,padding_y,padding_y,padding_x,padding_x,cv2.BORDER_CONSTANT,value=WHITE)
    return img


def main():
    parser = argparse.ArgumentParser(description='Deblur image')
    parser.add_argument('--data', help='Input data image')
    parser.add_argument('--output', help='Output image')
    args = parser.parse_args()
    input_name = args[0]
    destination_name = args[1]
    img = cv2.imread(input_name)
    img = add_padding(img)




if __name__ == '__main__':
    main()
