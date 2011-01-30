#!/usr/bin/env python

import scipy as sp
from scipy.sparse import coo_matrix

def accumarray(i, j, val=None):
    # hack from http://www.meliza.org/itoaeky/graphics.php?itemid=35
    # to provide functionality similar to matlab's accumarray

    if not val:
        val = sp.ones(len(i))

    return coo_matrix( (val, (i, j)) ).todense()


def train_test_split(X, y, frac=0.8):
    # number of examples
    N = y.shape[0]

    # shuffle example digits
    ndx = sp.random.permutation(N)
    X = X[ndx,:]
    y = y[ndx,:]

    # number of training examples as fraction of total
    Ntrain = int(frac*N)

    # split data into training and test sets
    Xtrain = X[:Ntrain,:]
    ytrain = y[:Ntrain]

    Xtest = X[Ntrain:,:]
    ytest = y[Ntrain:]

    return (Xtrain, ytrain, Xtest, ytest)
