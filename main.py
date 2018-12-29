from Images import Images
from Blob import Blob
import cv2

out_folder = "./out" 
in_folder = "./in"

images_obj = Images(out_folder, count=1)

min_region_area = 80

def changeMinArea(val):
    global min_region_area
    min_region_area = val

cv2.namedWindow("Letter Detection", cv2.WINDOW_AUTOSIZE)
cv2.createTrackbar('Min Area', 'Letter Detection', min_region_area, 300, changeMinArea)

for img_name, img in images_obj.images.items():
    img = cv2.resize(img, (0,0), fx=2, fy=2)
    while True:
        b_boxes = Blob(img).getBoundingBox(region_area=min_region_area)
        detected_img = img.copy()
        detected_img = cv2.cvtColor(detected_img, cv2.COLOR_GRAY2BGR)
        for minr, minc, maxr, maxc in b_boxes:
            cv2.rectangle(detected_img,(minc, minr),(maxc, maxr),(0,0,255),2)

        cv2.imshow('Letter Detection', detected_img)

        # Exit when Esc is pressed
        k = cv2.waitKey(1) & 0xFF
        # Save individual image when s is pressed
        # if k == ord("s"):
            # images_obj.save_image(out_folder + img_name, detected_img)
        if k == ord("q") or k == 27:
            break
