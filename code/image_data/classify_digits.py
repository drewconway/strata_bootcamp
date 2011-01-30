#!/usr/bin/env python

import scipy as sp
import matplotlib.pyplot as plt
import matplotlib.cm as cm

from digits import *
from knn import *
from mltools import *


if __name__=='__main__':

    # set seed so we all see the same random data
    sp.random.seed(20110201)

    # read digit data
    X, y = read_digits()

    # generate a random train/test split
    Xtrain, ytrain, Xtest, ytest = train_test_split(X, y, 0.8)
    del X, y

    # build nearest-neighbors classifier on training data
    classifier = KNN()
    classifier.add_examples(Xtrain, ytrain)
    classifier.train()

    # generate predictions for test data
    print "classifying test examples"
    ypred = classifier.predict(Xtest, k=1)

    # compute confusion matrix 
    confmat = accumarray( ytest, ypred )
    acc = confmat.diagonal().sum() / confmat.sum()
    print "confusion matrix:"
    print confmat
    print "accuracy:" , acc
    # accuracy directly:
    # print sp.mean( sp.around(ypred) == ytest )

    # generate heatmap of confusion matrix
    plt.imshow(confmat, interpolation='nearest')
    #plt.imshow(sp.log10(confmat+1), cmap=cm.hot, interpolation='nearest')
    plt.xlabel('actual')
    plt.ylabel('predicted')
    plt.colorbar()

    # save confusion matrix image
    print "saving digits_confmat.png"
    plt.savefig('digits_confmat.png')
    #plt.show()
