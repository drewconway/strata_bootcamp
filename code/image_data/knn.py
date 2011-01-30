#!/usr/bin/env python

import scipy as sp
import scipy.spatial as spat
import matplotlib.pyplot as plt
from scipy.stats import mode

class KNN():

    def __init__(self, X=None, y=None):
        if X and y:
            # add training data if provided
            self.add_examples(X, y)

    def add_examples(self, X, y):
        # memorize training data
        try:
            self.X = sp.vstack((self.X, X))
            self.y = sp.concatenate((self.y, y))
        except AttributeError:
            self.X = X
            self.y = y
            
    def train(self):
        # do nothing
        return
    
    def predict(self, X, k=1):
        # coerce test examples to be N-by-2 scipy array
        X = sp.array(X, ndmin=2)
        # number of test examples
        N = X.shape[0]

        # create empty vector for predictions
        yhat = sp.zeros(N)

        # use the cdist function to quickly compute distances
        # between all test and training examples
        D = spat.distance.cdist(X, self.X, 'euclidean')

        for i in range(N):
            # grab the indices of the k closest points
            ndx = D[i,:].argsort()[:k]

            # take a majority vote over the nearest points' labels
            yhat[i] = mode(self.y[ndx])[0]
            
        return yhat

class KNNKDTree(KNN):

    def train(self):
        # build kd-tree for quick lookup
        self.kdtree = spat.KDTree(self.X)
        
    def predict(self, X, k=1):
        # coerce test examples to be N-by-2 scipy array
        X = sp.array(X, ndmin=2)
        # number of test examples
        N = X.shape[0]

        # create empty vector for predictions
        yhat = sp.zeros(N)

        # use the kd-tree query function to quickly lookup nearest
        # neighbors
        D, ndx = self.kdtree.query(X, k=k)
        for i in range(N):
            # take a majority vote over the nearest points' labels
            yhat[i] = mode(self.y[ndx])[0]

        return yhat


if __name__=='__main__':
    # number of examples (N) and dimensions (D)
    N = 100
    D = 2

    # set seed so we all see the same random data
    sp.random.seed(20110201)

    # todo: help functions for synthetic data

    # generate N examples from class "0" and
    # N examples from class "1"
    # from normal distributions with different means
    y = sp.concatenate( (sp.zeros(N),
                         sp.ones(N)) )
    X = sp.vstack( (sp.random.randn(N,D) + [1, 1],
                    sp.random.randn(N,D) - [1, 1]) )

    # plot training data
    ndx = sp.where(y == 0)
    plt.plot(X[ndx,0], X[ndx,1], 'rx', alpha=0.25)
    ndx = sp.where(y == 1)
    plt.plot(X[ndx,0], X[ndx,1], 'bo', alpha=0.25)

    # build and train k-nearest neighbor classifier
    classifier = KNN()
    classifier.add_examples(X, y)
    classifier.train()

    # generate two easy-to-classify test examples
    Xtest = sp.array([[0.75, 0.75],
                      [-0.75, -0.75]])
    ytest = classifier.predict(Xtest, k=3)

    # plot test examples with predicted labels
    ndx = sp.where(ytest == 0)
    plt.plot(Xtest[ndx,0], Xtest[ndx,1], 'rx', alpha=1)
    ndx = sp.where(ytest == 1)
    plt.plot(Xtest[ndx,0], Xtest[ndx,1], 'bo', alpha=1)
    
    plt.show()
