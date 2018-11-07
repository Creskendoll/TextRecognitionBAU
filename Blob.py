from skimage.filters import threshold_otsu
from skimage.segmentation import clear_border
from skimage.measure import label, regionprops
from skimage.morphology import closing, square
from skimage.color import label2rgb

import matplotlib.patches as mpatches

class Blob(object):
    # input image must be BW
    def __init__(self, image_bw, thresh=100):
        # remove artifacts connected to image border
        cleared = clear_border(image_bw)

        # label image regions
        self.label_image = label(cleared)
        image_label_overlay = label2rgb(self.label_image, image=image_bw)
        self.labeled_image = image_label_overlay

    def getBoundingBox(self, region_area=100):
        for region in regionprops(self.label_image):
            # take regions with large enough areas
            if region.area >= region_area:
                # draw rectangle around segmented coins
                minr, minc, maxr, maxc = region.bbox
                yield mpatches.Rectangle((minc, minr), maxc - minc, maxr - minr,
                                        fill=False, edgecolor='red', linewidth=2)
