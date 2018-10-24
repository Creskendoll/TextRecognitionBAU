import os
import cv2
import numpy as np
from matplotlib import pyplot as plt

in_folder = "./in/"
out_folder = "./out/"
max_binary_threshold = 255
binary_threshold = 120
dilatation_size = 1
canny_min = 200
canny_max = 250

def changeBinaryThreshold(val):
    global binary_threshold
    binary_threshold = val

def changeCannyMin(val):
    global canny_min
    canny_min = val

def changeCannyMax(val):
    global canny_max
    canny_max = val

def changeDilationSize(val):
    global dilatation_size
    dilatation_size = val


cv2.namedWindow("Images", cv2.WINDOW_AUTOSIZE)

cv2.createTrackbar('Binary Threshold', 'Images', 120, max_binary_threshold, changeBinaryThreshold)
cv2.createTrackbar('Canny Min', 'Images', 200, 900, changeCannyMin)
cv2.createTrackbar('Canny Max', 'Images', 250, 900, changeCannyMax)
cv2.createTrackbar('Dilation Size', 'Images', dilatation_size, 20, changeDilationSize)

for root, dirs, files in os.walk(in_folder):
    for file_name in files:
        print("Processing:", file_name)
            
        # Read and convert the image to grayscale
        img_gray = cv2.imread(os.path.join(root, file_name), cv2.IMREAD_GRAYSCALE)
        if img_gray is None:
            print('Could not open or find the image: ', file_name)
            exit(0)
        # Convert image to binary
        # Automaticly determines threshold 
        # (binary_threshold, img_binary) = cv2.threshold(img_gray, 128, 255, cv2.THRESH_BINARY | cv2.THRESH_OTSU)
        # uses the defined threshold 
        img_binary = cv2.threshold(img_gray, binary_threshold, 255, cv2.THRESH_BINARY)[1]

        # Values from the example online
        # TODO: Explain wtf the canny values do
        # https://docs.opencv.org/3.1.0/da/d22/tutorial_py_canny.html
        # Edge detection
        laplacian_edge = cv2.Laplacian(img_binary,cv2.CV_64F)
        sobelx_edge = cv2.Sobel(img_binary,cv2.CV_64F,1,0,ksize=5)  # x
        sobely_edge = cv2.Sobel(img_binary,cv2.CV_64F,0,1,ksize=5)  # y

        # Show cv2 windows with trackbars n shit
        while True:
            canny_edge = cv2.Canny(img_gray, canny_min, canny_max)
            # Dilation 
            # https://docs.opencv.org/3.4/db/df6/tutorial_erosion_dilatation.html
            element = cv2.getStructuringElement(cv2.MORPH_RECT, (2*dilatation_size+1, 2*dilatation_size+1), (dilatation_size, dilatation_size))
            dilatation_dst = cv2.dilate(canny_edge, element)
            cv2.imshow('Images', dilatation_dst)
            # Exit when Esc is pressed
            k = cv2.waitKey(1) & 0xFF
            if k == 27: 
                break

        # Show images
        # plt.subplot(131),plt.imshow(img_gray, cmap=plt.cm.binary)
        # plt.title('Gray Image'), plt.xticks([]), plt.yticks([])
        # plt.subplot(132),plt.imshow(canny_edge, cmap='gray')
        # plt.title('Edge Image'), plt.xticks([]), plt.yticks([])
        # plt.subplot(133),plt.imshow(dilatation_dst, cmap='gray')
        # plt.title('Dilated Image'), plt.xticks([]), plt.yticks([])
        # plt.show()



