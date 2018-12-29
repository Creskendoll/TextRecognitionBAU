from skimage.segmentation import clear_border
from skimage.measure import label, regionprops

class Blob(object):
    # input image must be BW
    def __init__(self, image_bw):
        # remove artifacts connected to image border
        cleared = clear_border(image_bw)
        # label image regions
        self.label_image = label(cleared)

    def getBoundingBox(self, region_area=80):
        for region in regionprops(self.label_image):
            # take regions with large enough areas
            if region.area >= region_area:
                yield region.bbox
