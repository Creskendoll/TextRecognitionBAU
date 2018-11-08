import os
import cv2
import numpy as np
from matplotlib import pyplot as plt
from Images import Images
import scipy as sp
import scipy.ndimage

in_folder = "./in/"
out_folder = "./out/"
binary_threshold = 120
dilatation_size = 1
fill = 1
canny_min = 300
canny_max = 500

# Set {count} optional variable to read that many images
# Read all images available
images_obj = Images(in_folder, grayscale=True, count=1)

global_img = None
refPt = []

def changeFill(val):
    global fill
    fill = val

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

cv2.createTrackbar('Binary Threshold', 'Images', binary_threshold, 255, changeBinaryThreshold)
cv2.createTrackbar('Canny Min', 'Images', canny_min, 900, changeCannyMin)
cv2.createTrackbar('Canny Max', 'Images', canny_max, 900, changeCannyMax)
cv2.createTrackbar('Dilation Size', 'Images', 2, 5, changeDilationSize)
cv2.createTrackbar('Fill', 'Images', fill, 1, changeFill)

# Uncomment this if u want to utilize mouse clicks
# cv2.setMouseCallback("Images", click)

# fill holes in img
def flood_fill(img,h_max=255):
    input_array = np.copy(img) 
    el = sp.ndimage.generate_binary_structure(2,2).astype(np.int)
    inside_mask = sp.ndimage.binary_erosion(~np.isnan(input_array), structure=el)
    output_array = np.copy(input_array)
    output_array[inside_mask]=h_max
    output_old_array = np.copy(input_array)
    output_old_array.fill(0)   
    el = sp.ndimage.generate_binary_structure(2,1).astype(np.int)
    while not np.array_equal(output_old_array, output_array):
        output_old_array = np.copy(output_array)
        output_array = np.maximum(input_array,sp.ndimage.grey_erosion(output_array, footprint=el))
    return output_array

# define all pre processing stuff under this function
def apply_pre_processing(image, resize_by=1):
    # so that we don't alter the original image
    new_image = image.copy()

    new_image = cv2.resize(new_image, (0,0), fx=resize_by, fy=resize_by)
    
    # Easy way
    # ret,th = cv2.threshold(new_image,0,255,cv2.THRESH_BINARY+cv2.THRESH_OTSU)
    # return th

    # TODO: Explain wtf the canny values do
    # https://docs.opencv.org/3.1.0/da/d22/tutorial_py_canny.html
    # Note: We got rid of laplacian and sobel since we won't necesseraly talk about them in our report
    # Sobel we will but it will be covered under Canny
    # Edge detection
    canny_edge_img = cv2.Canny(new_image, canny_min, canny_max)
    
    # Dilation
    # https://docs.opencv.org/3.4/db/df6/tutorial_erosion_dilatation.html
    element = cv2.getStructuringElement(cv2.MORPH_DILATE, (dilatation_size+1, dilatation_size+1), (dilatation_size, dilatation_size))
    new_image = cv2.dilate(canny_edge_img, element)

    return new_image

def apply_to_all_and_save():
    for img_name, im in images_obj.images.items():
        p_im = flood_fill(apply_pre_processing(im)) 
        images_obj.save_image(out_folder + img_name, p_im)

for img_name, img in images_obj.images.items():
    print("Showing image:", img_name)
    # new_image = new_image[240:320, 670:1250] # RoI
    img = img[250:300, 680:1230] # RoI

    resize_img_by = 2
    
    img = cv2.resize(img, (0,0), fx=resize_img_by, fy=resize_img_by)

    # Show cv2 windows with trackbars n shit
    while True:
        # for mouse clicks
        # global_img = processed_image
        processed_image = apply_pre_processing(img)

        if fill == 1:
            processed_image = flood_fill(processed_image)

        # OTSU is automatic
        # This is manual thresholding 
        _,bin_image = cv2.threshold(img,binary_threshold,255,cv2.THRESH_BINARY)
    
        # original, grayscale, binary, canny
        stacked_image = np.vstack((img, bin_image, processed_image))
        
        cv2.imshow('Images', stacked_image)

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
