#!/usr/bin/env python

import scipy as sp
import matplotlib.image as mpimg
import matplotlib.pyplot as plt
import scipy.cluster.vq as spvq
import matplotlib.cm as cm

if __name__=='__main__':
    K = 7

    sp.random.seed(20110201)

    I = mpimg.imread('flickr_vivid/68826730.jpg')
    X = sp.reshape(I, (-1,3), order='F')
    centers, err = spvq.kmeans(X, K)
    assignments, err = spvq.vq(X, centers)

    plt.subplot(131)
    plt.imshow(I, cmap=cm.gray, interpolation='nearest', origin='lower')

    plt.subplot(132)
    Iseg = sp.reshape(assignments, (75,75)).transpose()
    plt.imshow(Iseg, cmap=cm.gray, interpolation='nearest', origin='lower')

    plt.subplot(133)
    Z = centers[assignments]

    Icomp = sp.reshape(Z, (75,75,3), order='F')
    plt.imshow(Icomp, interpolation='nearest', origin='lower')
    
    plt.show()

    # todo: add 3-d rgb plot
