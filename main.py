from Images import Images
from Blob import Blob
import matplotlib.pyplot as plt

out_folder = "./out" 
in_folder = "./in"

if __name__ == "main":
    images_obj = Images(out_folder)
    for img_name, img in images_obj.images.items():
        blob = Blob(img)
        b_boxes = blob.getBoundingBox()
