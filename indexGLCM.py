import cv2
import numpy as np
import os
import glob
import Descriptors
import argparse

# Create the argument parser to parse the arguments
ap = argparse.ArgumentParser()

# Switch for the path to our photos directory
ap.add_argument("-d", "--dataset", required=True, help="Path to directory that contains images")
ap.add_argument("-i", "--index", required=True, help="Path to where the index will be stored")
args = vars(ap.parse_args())

cmd = Descriptors.GLCM()


output = open(args["index"], "w")

# Using glob to get path of images and go through all of them
for imagePath in glob.glob(args["dataset"] + "/*.jpg"):
    imageUID = imagePath[imagePath.rfind("/") + 1:]
    image = cv2.imread(imagePath)
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    features = cmd.extract_features(gray)
    features = [str(f) for f in features]
    output.write("%s,%s\n" % (imageUID, ",".join(features)))


output.close()




