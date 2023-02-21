import numpy as np
import csv

class Searcher:
    def __init__(self ,indexPath):
        # storing the index
        self.indexPath = indexPath

    def search(self ,queryFeatures,limit=40):
        # make a dictionary for the results
        results = {}
        distance=[]
        # open the index file for reading
        with open(self.indexPath) as f:
            # initializing the csv reader
            reader = csv.reader(f)

            # loop over the rows in the index
            for row in reader:
                # parse out the imageID and features, then calculate the chi-squared distance between the saved features and the features of our image
                features = [float(x) for x in row[1:]]
                d = self.chi2_distance(features, queryFeatures)

                # now we have the distance between the two feature vectors. we now update the results dictionary
                results[row[0]] = d

            # closing the reader
            f.close()

        # sort the results such that the dictionary starts with smaller values as they will be closest to the given image
        results = sorted([(v ,k) for (k ,v) in results.items()])

        # return our results
        return results[:limit]

    def chi2_distance(self, histA, histB, eps = 1e-10):
        # calculating the chi squared distance
        d = 0.5 * np.sum([(( a -b) ** 2) / (a + b + eps) for (a, b) in zip(histA, histB)])

        # return the chi squared distance
        return d
    def Euclidean_distance(self,p, q):
        dist = np.sqrt(np.sum(np.square(p-q)))
        return dist

class SearcherRGB:
    def __init__(self ,indexPath):
        # storing the index
        self.indexPath = indexPath

    def search(self ,queryFeatures,limit=40):
        # make a dictionary for the results
        results = {}
        distance=[]
        # open the index file for reading
        with open(self.indexPath) as f:
            # initializing the csv reader
            reader = csv.reader(f)

            # loop over the rows in the index
            for row in reader:
                # parse out the imageID and features, then calculate the chi-squared distance between the saved features and the features of our image
                features = [float(x) for x in row[1:]]
                d = self.Euclidean_distance(features, queryFeatures)

                # now we have the distance between the two feature vectors. we now update the results dictionary
                results[row[0]] = d

            # closing the reader
            f.close()

        # sort the results such that the dictionary starts with smaller values as they will be closest to the given image
        results = sorted([(v ,k) for (k ,v) in results.items()])

        # return our results
        return results[:limit]

    def chi2_distance(self, histA, histB, eps = 1e-10):
        # calculating the chi squared distance
        d = 0.5 * np.sum([(( a -b) ** 2) / (a + b + eps) for (a, b) in zip(histA, histB)])

        # return the chi squared distance
        return d
    def Euclidean_distance(self,p, q):
        dist = np.sqrt(np.sum(np.square(p-q)))
        return dist

class SearcherHu:
    def __init__(self ,indexPath):
        # storing the index
        self.indexPath = indexPath

    def search(self ,queryFeatures,limit=40):
        # make a dictionary for thr results
        results = {}

        # open the index file for reading
        with open(self.indexPath) as f:
            # initializing the csv reader
            reader = csv.reader(f)

            # loop over the rows in the index
            for row in reader:
                # parse out the imageID and features, then calculate the chi-squared distance between the saved features and the features of our image
                features = [float(x[1:len(x)-1]) for x in row[1:]]
                d = self.chi2_distance(features, queryFeatures)

                # now we have the distance between the two feature vectors. we now update the results dictionary
                results[row[0]] = d

            # closing the reader
            f.close()

        # sort the results such that the dictionary starts with smaller values as they will be closest to the given image
        results = sorted([(v ,k) for (k ,v) in results.items()])

        # return our results
        return results[:limit]

    def chi2_distance(self, histA, histB, eps = 1e-10):
        # calculating the chi squared distance
        d = 0.5 * np.sum([(( a -b) ** 2) / (a + b + eps) for (a, b) in zip(histA, histB)])

        # return the chi squared distance
        return d
    def Euclidean_distance(self,p, q):
        dist = np.sqrt(np.sum(np.square(p-q)))
        return dist

class SearcherCombo:
    def __init__(self ,indexPath1,indexPath2,w1,w2):
        # storing the index
        self.indexPath1 = indexPath1
        self.indexPath2 = indexPath2
        self.w1=w1
        self.w2=w2

    def search(self ,queryFeatures1,queryFeatures2,limit=30):
        # make a dictionary for the results
        results = {}
        distance=[]
        # open the index file for reading
        with open(self.indexPath1) as f1,open(self.indexPath2) as f2:
            # initializing the csv reader
            reader1 = csv.reader(f1)
            reader2= csv.reader(f2)

            # loop over the rows in the index
            for row1, row2 in zip(reader1, reader2):
                # parse out the imageID and features, then calculate the chi-squared distance between the saved features and the features of our image
                features1 = [float(x) for x in row1[1:]]
                features2 = [float(x) for x in row2[1:]]
                d1 = self.chi2_distance(features1, queryFeatures1)
                d2 = self.chi2_distance(features2, queryFeatures2)
                d=self.w1*d1+self.w2*d2
                # now we have the distance between the two feature vectors. we now update the results dictionary
                results[row1[0]] = d

            # closing the reader
            f1.close()
            f2.close()

        # sort the results such that the dictionary starts with smaller values as they will be closest to the given image
        results = sorted([(v ,k) for (k ,v) in results.items()])

        # return our results
        return results[:limit]

    def chi2_distance(self, histA, histB, eps = 1e-10):
        # calculating the chi squared distance
        d = 0.5 * np.sum([(( a -b) ** 2) / (a + b + eps) for (a, b) in zip(histA, histB)])

        # return the chi squared distance
        return d
    def Euclidean_distance(self,p, q):
        dist = np.sqrt(np.sum(np.square(p-q)))
        return dist


class SearcherComboTrois:
    def __init__(self ,indexPath1,indexPath2,indexPath3,w1,w2,w3):
        # storing the index
        self.indexPath1 = indexPath1
        self.indexPath2 = indexPath2
        self.indexPath3 = indexPath3
        self.w1=w1
        self.w2=w2
        self.w3=w3

    def search(self ,queryFeatures1,queryFeatures2,queryFeatures3,limit=30):
        # make a dictionary for the results
        results = {}
        distance=[]
        # open the index file for reading
        with open(self.indexPath1) as f1,open(self.indexPath2) as f2,open(self.indexPath3) as f3:
            # initializing the csv reader
            reader1 = csv.reader(f1)
            reader2= csv.reader(f2)
            reader3= csv.reader(f3)

            # loop over the rows in the index
            for row1,row2,row3 in zip(reader1, reader2,reader3):
                # parse out the imageID and features, then calculate the chi-squared distance between the saved features and the features of our image
                #features1 = [float(x) for x in row1[1:]]
                features1 = [float(x[1:len(x)-1]) for x in row1[1:]]
                features2 = [float(x) for x in row2[1:]]
                features3 = [float(x) for x in row3[1:]]
                d1 = self.chi2_distance(features1, queryFeatures1)
                d2 = self.chi2_distance(features2, queryFeatures2)
                d3 = self.chi2_distance(features3, queryFeatures3)
                d=self.w1*d1+self.w2*d2+self.w3*d3
                # now we have the distance between the two feature vectors. we now update the results dictionary
                results[row1[0]] = d

            # closing the reader
            f1.close()
            f2.close()

        # sort the results such that the dictionary starts with smaller values as they will be closest to the given image
        results = sorted([(v ,k) for (k ,v) in results.items()])

        # return our results
        return results[:limit]

    def chi2_distance(self, histA, histB, eps = 1e-10):
        # calculating the chi squared distance
        d = 0.5 * np.sum([(( a -b) ** 2) / (a + b + eps) for (a, b) in zip(histA, histB)])

        # return the chi squared distance
        return d
    def Euclidean_distance(self,p, q):
        dist = np.sqrt(np.sum(np.square(p-q)))
        return dist

class SearcherCombo1:
    def __init__(self ,indexPath1,indexPath2,w1,w2):
        # storing the index
        self.indexPath1 = indexPath1
        self.indexPath2 = indexPath2
        self.w1=w1
        self.w2=w2

    def search(self ,queryFeatures1,queryFeatures2,limit=30):
        # make a dictionary for the results
        results = {}
        distance=[]
        # open the index file for reading
        with open(self.indexPath1) as f1,open(self.indexPath2) as f2:
            # initializing the csv reader
            reader1 = csv.reader(f1)
            reader2= csv.reader(f2)

            # loop over the rows in the index
            for row1, row2 in zip(reader1, reader2):
                # parse out the imageID and features, then calculate the chi-squared distance between the saved features and the features of our image
                #features1 = [float(x) for x in row1[1:]]
                features1 = [float(x[1:len(x)-1]) for x in row1[1:]]
                features2 = [float(x) for x in row2[1:]]
                d1 = self.chi2_distance(features1, queryFeatures1)
                d2 = self.chi2_distance(features2, queryFeatures2)
                d=self.w1*d1+self.w2*d2
                # now we have the distance between the two feature vectors. we now update the results dictionary
                results[row1[0]] = d

            # closing the reader
            f1.close()
            f2.close()

        # sort the results such that the dictionary starts with smaller values as they will be closest to the given image
        results = sorted([(v ,k) for (k ,v) in results.items()])

        # return our results
        return results[:limit]

    def chi2_distance(self, histA, histB, eps = 1e-10):
        # calculating the chi squared distance
        d = 0.5 * np.sum([(( a -b) ** 2) / (a + b + eps) for (a, b) in zip(histA, histB)])

        # return the chi squared distance
        return d
    def Euclidean_distance(self,p, q):
        dist = np.sqrt(np.sum(np.square(p-q)))
        return dist
