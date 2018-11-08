from Images import Images
from Blob import Blob
import matplotlib.pyplot as plt
import cv2

out_folder = "./out" 
in_folder = "./in"
fig,ax = plt.subplots(1)
images_obj = Images(out_folder, count=1)

for img_name, img in images_obj.images.items():
    img = cv2.resize(img, (0,0), fx=2, fy=2)
    blob = Blob(img)
    b_boxes = blob.getBoundingBox()
    ax.imshow(img, cmap=plt.cm.binary)
    for rect in b_boxes:
        ax.add_patch(rect)
    plt.show()

