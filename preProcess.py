import os
import cv2
import numpy as np
from matplotlib import pyplot as plt
from Images import Images

in_folder = "./in/"
out_folder = "./out/"
max_binary_threshold = 255
binary_threshold = 120
dilatation_size = 1
canny_min = 200
canny_max = 250

# Set {count} optional variable to read that many images 
# Read all images available
images_obj = Images(in_folder)

global_img = None
refPt = []

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

# Process clicks on the image 
# must be set to a callback in order to work
# cv2.setMouseCallback("Images", click) (see below)
def click(event, x, y, flags, param):
    global global_img, refPt
    if event == cv2.EVENT_LBUTTONDOWN:
        # record first (x, y)
        refPt = [(x, y)]
    elif event == cv2.EVENT_LBUTTONUP:
        # record the ending (x, y)
        refPt.append((x, y))
        print("Click Up", refPt)
        # draw a rectangle around the region of interest
        # works a bit weird with grayscale 
        cv2.rectangle(global_img, refPt[0], refPt[1], (255, 255, 255), 6)

cv2.namedWindow("Images", cv2.WINDOW_AUTOSIZE)

cv2.createTrackbar('Binary Threshold', 'Images', 120, max_binary_threshold, changeBinaryThreshold)
cv2.createTrackbar('Canny Min', 'Images', 200, 900, changeCannyMin)
cv2.createTrackbar('Canny Max', 'Images', 250, 900, changeCannyMax)
cv2.createTrackbar('Dilation Size', 'Images', 2, 5, changeDilationSize)

# Uncomment this if u want to utilize mouse clicks  
# cv2.setMouseCallback("Images", click)

# define all pre processing stuff under this function
def apply_pre_processing(image, resize_by=1, binary=False):
    # so that we don't alter the original image
    new_image = image.copy()

    new_image = new_image[240:320, 670:1250] # RoI

    new_image = cv2.resize(new_image, (0,0), fx=resize_by, fy=resize_by) 

    # Convert image to binary
    # Automaticly determines threshold 
    # uses the defined threshold 
    if binary:
        # (binary_threshold, img_binary) = cv2.threshold(img, 128, 255, cv2.THRESH_BINARY | cv2.THRESH_OTSU)
        new_image = cv2.threshold(new_image, binary_threshold, 255, cv2.THRESH_BINARY)[1]

    # TODO: Explain wtf the canny values do
    # https://docs.opencv.org/3.1.0/da/d22/tutorial_py_canny.html
    # Note: We got rid of laplacian and sobel since we won't necesseraly talk about them in our report
    # Sobel we will but it will be covered under Canny 
    # Edge detection
    canny_edge_img = cv2.Canny(new_image, canny_min, canny_max)

    # Dilation 
    # https://docs.opencv.org/3.4/db/df6/tutorial_erosion_dilatation.html
    element = cv2.getStructuringElement(cv2.MORPH_DILATE, (2*dilatation_size+1, 2*dilatation_size+1), (dilatation_size, dilatation_size))
    new_image = cv2.dilate(canny_edge_img, element)

    # Show images if needed
    # plt.subplot(131),plt.imshow(img_gray, cmap=plt.cm.binary)
    # plt.title('Gray Image'), plt.xticks([]), plt.yticks([])
    # plt.subplot(132),plt.imshow(canny_edge, cmap='gray')
    # plt.title('Edge Image'), plt.xticks([]), plt.yticks([])
    # plt.subplot(133),plt.imshow(dilatation_dst, cmap='gray')
    # plt.title('Dilated Image'), plt.xticks([]), plt.yticks([])
    # plt.show()

    return new_image

def apply_to_all_and_save():
    for img_name, img in images_obj.images.items():
        images_obj.save_image(out_folder + img_name, apply_pre_processing(img))


for img_name, img in images_obj.images.items():
    print("Showing image:", img_name)

    # Show cv2 windows with trackbars n shit
    while True:
        processed_image = apply_pre_processing(img, resize_by=3)
        
        # for mouse clicks
        # global_img = processed_image
        
        cv2.imshow('Images', processed_image)

        # Exit when Esc is pressed
        k = cv2.waitKey(1) & 0xFF
        # Save individual image when s is pressed 
        if k == ord("s"):
            images_obj.save_image(out_folder + img_name, processed_image)
        # (p)rocess and save all the images in the in folder to the our folder  
        if k == ord("p"):
            apply_to_all_and_save()
        if k == ord("q") or k == 27:
            break
