# import the necessary packages
import Descriptors
import argparse
import glob
import cv2

# Create the argument parser to parse the arguments
ap = argparse.ArgumentParser()

# Switch for the path to our photos directory
ap.add_argument("-d", "--dataset", required=True, help="Path to directory that contains images")
ap.add_argument("-i", "--index", required=True, help="Path to where the index will be stored")
args = vars(ap.parse_args())

# Initializing our color descriptor
hd = Descriptors.HuMoments()

# open the output index file for writing
output = open(args["index"], "w")

# Using glob to get path of images and go through all of them
for imagePath in glob.glob(args["dataset"] + "/*.jpg"):
    imageUID = imagePath[imagePath.rfind("/") + 1:]
    image= cv2.imread(imagePath,cv2.IMREAD_GRAYSCALE)
    features = hd.hu_moments(image)
    features = [str(f) for f in features]
    output.write("%s,%s\n" % (imageUID, ",".join(features)))
output.close()

