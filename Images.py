import os
import cv2

# an in memory object whioch lets us access images much faster than we'd do with reading them out of disk
# costs a little time at statup
# {count} optional variable can be set to read defined number of images, -1 is for all
class Images(object):
    # Load the images in folder
    def __init__(self, folder_name, grayscale=True, sub_folders=False, count=-1):
        # create a dictionary of images with their names and actual data
        self.images = {}
        # define directories depending on how many folders we wanna dig in to
        if sub_folders:
            directories = os.walk(folder_name)
        else:
            directories = self.walklevel(folder_name)

        print("Loading folder:", os.path.abspath(folder_name))
        for root, dirs, files in directories:
            if count != -1:
                print("Loading %d out of %d files." % (count, len(files)))
            else:
                print("Loading all of %d files." % len(files))

            for file_name in files:
                if count != 0:
                    count = count - 1
                    if grayscale:
                        img = cv2.imread(os.path.join(root, file_name), cv2.IMREAD_GRAYSCALE)
                    else:
                        img = cv2.imread(os.path.join(root, file_name), cv2.IMREAD_COLOR)
                    
                    if img is None:
                        print("Could not read image:", file_name)
                    else:
                        # save name and data to the data itself so that it's faster to read from memory
                        self.images[file_name] = img
    
    def save_all_images(self, path):
        for image_name in self.images.keys():
            self.save_image_by_name(path, img_name)

    def save_image_by_name(self, path, image_name):
        if not os.path.isdir(path):
            print("Creating directory:", os.path.abspath(path))
            os.mkdir(path)
        out_file_name = image_name.split(".")[0] + "_out.png"
        print("Saving image as:", out_file_name) 
        cv2.imwrite(path + out_file_name, self.images[image_name])

    # path includes the file name
    def save_image(self, path, image):
        directory = os.path.dirname(path)
        if not os.path.isdir(directory):
            print("Creating directory:", os.path.abspath(directory))
            os.mkdir(directory)
        # Edit this line if you wanna change output name
        out_file_name = path[len(directory)+1:].split(".")[0] + "_out.png"
        print("Saving image as:", out_file_name) 
        cv2.imwrite(os.path.join(directory, out_file_name), image)

    # window name is the name given in cv2.namedWindow({name}, flag)
    def show_image(self, window_name, image_name):
        img = self.images[image_name]
        if img is None:
            print("No image named %s in collection" % image_name)
        else:
            # create window if doesn't exist
            if cv2.getWindowProperty(window_name, 0) < 0:
                cv2.namedWindow(window_name, cv2.WINDOW_AUTOSIZE)
            cv2.imshow(window_name, img)

    # same with os.walk
    # level is how deep we wanna go in the recursion
    def walklevel(self, some_dir, level=1):
        some_dir = some_dir.rstrip(os.path.sep)
        if not os.path.isdir(some_dir):
            print("Creating directory:", os.path.abspath(some_dir))
            os.mkdir(some_dir)
        num_sep = some_dir.count(os.path.sep)
        for root, dirs, files in os.walk(some_dir):
            yield root, dirs, files
            num_sep_this = root.count(os.path.sep)
            if num_sep + level <= num_sep_this:
                del dirs[:]
                