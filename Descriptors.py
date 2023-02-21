import numpy as np
import cv2
import imutils
from skimage import feature


class ColorDescriptor:
    def __init__(self, bins):
        # Storing number of bins for histogram
        self.bins = bins

    def describe(self, image):
        # Convert the image into hsv and initialize the features to quantify the image
        #image = image.astype('uint8')
        image = cv2.cvtColor(image, cv2.COLOR_BGR2HSV)
        features = []

        # Obtaining the dimensions and center of the image
        (h, w) = image.shape[:2]
        (cX, cY) = (int(w * 0.5), int(h * 0.5))

        # Divide the image into 4 segements(top-left,top-right,bottom-left,bottom-right,center)
        segements = [(0, cX, 0, cY), (cX, w, 0, cY), (cX, w, cY, h), (0, cX, cY, h)]

        # Construct an eliptical mask representing the center of the image which is 75% of height and width of image
        (axesX, axesY) = (int(w * 0.75) // 2, int(h * 0.75) // 2)
        ellipMask = np.zeros(image.shape[:2], dtype="uint8")
        cv2.ellipse(ellipMask, (cX, cY), (axesX, axesY), 0, 0, 360, 255, -1)

        # Loop over the segements
        for (startX, endX, startY, endY) in segements:
            # Construct a mask for each corner of the image subtracting the elliptical center from it
            cornerMask = np.zeros(image.shape[:2], dtype="uint8")
            cv2.rectangle(cornerMask, (startX, startY), (endX, endY), 255, -1)
            cornerMask = cv2.subtract(cornerMask, ellipMask)

            # Extract a color histogram from the image and update the feature vector
            hist = self.histogram(image, cornerMask)
            features.extend(hist)

        # Extract a color histogram from the elliptical region and update the feature vector
        hist = self.histogram(image, ellipMask)
        features.extend(hist)

        # Return the feature vector
        return features

    def histogram(self, image, mask):

        # Extract a 3-D color histogram from the masked region of the image, using the number of bins supplied
        # print(image)
        hist = cv2.calcHist([image], [0, 1, 2], mask, self.bins, [0, 180, 0, 256, 0, 256])

        # Normalize the histogram
        if imutils.is_cv2():
            # For openCV version 2.4
            hist = cv2.normalize(hist).flatten()
        else:
            # For openCV version 3+
            hist = cv2.normalize(hist, hist).flatten()

        # Returning histogram
        return hist
    def RGB_hist(self,img,bins=128,norm='sum',factor=512):
        if (len(img.shape)==2):
            hist,=np.histogram(img,bins=bins)
        if (len(img.shape)==3):
            hist_R,_ = np.histogram(img[:,:,0],bins=bins)
            hist_G,_ = np.histogram(img[:,:,1],bins=bins)
            hist_B,_ = np.histogram(img[:,:,2],bins=bins)
            hist=np.concatenate([hist_R,hist_G,hist_B])
        hist=hist.astype(float)
        if(norm=='sum'):
            hist/=(hist.sum()+0.0001)
        return hist

class lbp:
    def __init__(self, radius,sampling_pixels):
        # Storing number of bins for histogram
        self.radius = radius
        self.sampling_pixels=sampling_pixels
    def lbp_features(self,img):
        if (len(img.shape) > 2):
            img = img.astype(float)
            img = img[:,:,0]*0.3 + img[:,:,1]*0.59 + img[:,:,2]*0.11

    
        img = img.astype(np.uint8)
    
   
        i_min = np.min(img)
        i_max = np.max(img)
        if (i_max - i_min != 0):
            img = (img - i_min)/(i_max-i_min)
    
    # compute LBP
        lbp = feature.local_binary_pattern(img, self.sampling_pixels, self.radius, method="uniform")
    
    # LBP returns a matrix with the codes, so we compute the histogram
        (hist, _) = np.histogram(lbp.ravel(), bins=np.arange(0, self.sampling_pixels + 3), range=(0, self.sampling_pixels + 2))

    # normalization
        hist = hist.astype("float")
        hist /= (hist.sum() + 1e-6)
    # return the histogram of Local Binary Patterns
        return hist

from math import copysign, log10

class HuMoments:
    def __init__(self):
        # Storing number of bins for histogram
        self=self
    def hu_moments(self,img):

        # Threshold image
        _,im = cv2.threshold(img, 128, 255, cv2.THRESH_BINARY)

        # Calculate Moments
        moment = cv2.moments(im)

        # Calculate Hu Moments
        huMoments = cv2.HuMoments(moment)
        for i in range(0,7):
            if (int(huMoments[i])==0):
                break    
            huMoments[i] = -1* copysign(1.0, huMoments[i]) * log10(abs(huMoments[i]))
        
        return huMoments



import mahotas as mt

class ZernikeMoments:
	def __init__(self, radius):
		# store the size of the radius that will be
		# used when computing moments
		self.radius = radius

	def describe(self, image):
		# return the Zernike moments for the image
		return mt.features.zernike_moments(image, self.radius)


class GLCM:
    def extract_features(self,image):
        # calculate haralick texture features for 4 types of adjacency
        textures = mt.features.haralick(image)

        # take the mean of it and return it
        ht_mean = textures.mean(axis=0)
        return ht_mean




    
