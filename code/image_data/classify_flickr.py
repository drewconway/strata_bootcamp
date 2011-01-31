#!/usr/bin/env python

import sys
import os.path
import scipy as sp
import matplotlib.image as mpimg
import matplotlib.pyplot as plt
from scipy.cluster.vq import whiten

from imgtools import *
from mltools import *
from knn import *

if __name__=='__main__':

    # default to classifying headshots vs landscapes
    bins = 16
    K = 9
    dirs = ['flickr_headshot','flickr_landscape']
    
    # take bins, number of neighbors, and image directories from command line
    try:
        bins = int(sys.argv[1])
        K = int(sys.argv[2])
        dirs = sys.argv[3:]
    except:
        pass

    print "using 3*%d bins for image intensity features" % bins

    # load images from each directory
    images = []
    for d, directory in enumerate(dirs):
        imagesd = read_image_dir(directory, '*.jpg')

        Xd = sp.array( [rgb_features(I, bins) for I in imagesd] )

        # create vector of labels
        yd = d*sp.ones(Xd.shape[0])

        try:
            # append digits and labels to X and y, respectively
            X = sp.vstack((X, Xd))
            y = sp.concatenate((y, yd))
        except NameError:
            # create X and y if they don't exist
            X = Xd
            y = yd

        images.append(imagesd)


    # set seed so we all see the same random numbers
    sp.random.seed(20110201)

    # generate a random train/test split
    Xtrain, ytrain, Xtest, ytest = train_test_split(X, y, 0.8)
    del X, y

    # normalize training features
    Xtrain = whiten(Xtrain)

    # "build" k-nearest neighbors classifier on training data
    print "building k-nearest neighbors classifier"
    classifier = KNN()
    classifier.add_examples(Xtrain, ytrain)
    classifier.train()

    # normalize test features
    Xtest = whiten(Xtest)

    Ks = range(1,K+1,2)
    accuracy = []
    for k in Ks:
        # generate predictions for test data
        ypred = classifier.predict(Xtest, k)

        # compute confusion matrix 
        confmat = accumarray( ytest, ypred )
        acc = confmat.diagonal().sum() / confmat.sum()
        print "k = %d, accuracy = %.4f" % (k,acc)

        accuracy.append(acc)

    plt.plot(Ks, accuracy, 'x--')
    plt.show()
    plt.xlabel('neighbors')
    plt.ylabel('accuracy')
