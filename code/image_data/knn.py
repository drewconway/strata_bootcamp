#!/usr/bin/env python

import scipy as sp
import scipy.spatial as spat
import matplotlib.pyplot as plt

class KNN():

    def __init__(self, y, X):
        self.y = y
        self.X = X

    def predict(self, X, k=1):
        X = sp.array(X, ndmin=2)
        N = X.shape[0]

        yhat = sp.zeros(N)
        D = spat.distance.cdist(X, self.X, 'euclidean')
        for i in range(N):
            ndx = D[i,:].argsort()[:k]

            yhat[i] = self.y[ndx].mean()

        return yhat

if __name__=='__main__':
    
    N = 100
    D = 2

    y = sp.vstack( (sp.zeros((N,1)),
                    sp.ones((N,1))) )
    X = sp.vstack( (sp.random.randn(N,D) + [1, 1],
                    sp.random.randn(N,D) - [1, 1]) )

    ndx, ig = sp.where(y == 0)
    plt.plot(X[ndx,0], X[ndx,1], 'rx', alpha=0.25)
    ndx, ig = sp.where(y == 1)
    plt.plot(X[ndx,0], X[ndx,1], 'bo', alpha=0.25)

    classifier = KNN(y, X)

    Xtest = sp.array([[1.5, 1],
                      [-1.5, -1]])
    ytest = classifier.predict(Xtest, k=3)

    ndx = sp.where(ytest == 0)
    plt.plot(Xtest[ndx,0], Xtest[ndx,1], 'rx', alpha=1)
    ndx = sp.where(ytest == 1)
    plt.plot(Xtest[ndx,0], Xtest[ndx,1], 'bo', alpha=1)
    
    plt.show()
