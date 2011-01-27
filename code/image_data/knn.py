#!/usr/bin/env python

import scipy as sp
import scipy.spatial as spat
import matplotlib.pyplot as plt

# todo: add_example(s)

class KNN():

    def __init__(self, y, X):
        # memorize training data
        self.y = y
        self.X = X

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

            # predict the mean of nearest points' labels
            yhat[i] = self.y[ndx].mean()

        return yhat

class KNNKDTree():

    def __init__(self, y, X):
        self.y = y
        self.X = X

    def train(self):
        # build kd-tree for quick lookup
        self.kdtree = spat.KDTree(X)
        
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
            # predict the mean of nearest points' labels
            yhat[i] = self.y[ndx[i]].mean()

        return yhat


if __name__=='__main__':
    # number of examples (N) and dimensions (D)
    N = 100
    D = 2

    # generate N examples from class "0" and
    # N examples from class "1"
    # from normal distributions with different means
    y = sp.vstack( (sp.zeros((N,1)),
                    sp.ones((N,1))) )
    X = sp.vstack( (sp.random.randn(N,D) + [1, 1],
                    sp.random.randn(N,D) - [1, 1]) )

    # plot training data
    ndx, ig = sp.where(y == 0)
    plt.plot(X[ndx,0], X[ndx,1], 'rx', alpha=0.25)
    ndx, ig = sp.where(y == 1)
    plt.plot(X[ndx,0], X[ndx,1], 'bo', alpha=0.25)

    # build and train k-nearest neighbor classifier
    classifier = KNNKDTree(y, X)
    classifier.train()

    # generate two easy-to-classify test examples
    Xtest = sp.array([[1.5, 1],
                      [-1.5, -1]])
    ytest = classifier.predict(Xtest, k=3)

    # plot test examples with predicted labels
    ndx = sp.where(ytest == 0)
    plt.plot(Xtest[ndx,0], Xtest[ndx,1], 'rx', alpha=1)
    ndx = sp.where(ytest == 1)
    plt.plot(Xtest[ndx,0], Xtest[ndx,1], 'bo', alpha=1)
    
    plt.show()
