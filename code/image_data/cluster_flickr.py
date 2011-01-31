#!/usr/bin/env python

import scipy as sp
import scipy.cluster.vq as spvq
import matplotlib.image as mpimg
import matplotlib.pyplot as plt
import glob
from math import sqrt, ceil

from imgtools import *

def plot_montage(images, ndx, ncol=None):

    N = len(ndx)
    
    if not ncol:
        ncol = int(sqrt(N))

    f = plt.figure(dpi=100)
    
    row = 0
    col = 0
    for i in range(N):

        I = sp.array(images[ndx[i]], dtype='float32')
        I = I / I.max()
        
        height = I.shape[0]
        width = I.shape[1]
        ax = plt.figimage(I, xo=width*col, yo=height*row, origin='lower')

        col += 1
        if col % ncol == 0:
            row += 1
            col = 0

    f.set_figheight(row*height/100)
    f.set_figwidth(ncol*width/100)

    return f

if __name__=='__main__':

    directory = 'flickr_vivid'
    bins = 10
    K = 3
    
    pattern = '%s/*.jpg' % directory
    print pattern
    fnames = glob.glob(pattern)

    N = len(fnames)
    print "reading %d image files from %s" % (N, directory)
    X = sp.zeros( (0,3*bins) )
    images = []
    for i, fname in enumerate(fnames):
        try:
            I = mpimg.imread(fname)

            X = sp.vstack( (X, rgb_features(I, bins)) )
            images.append(I)
            
        except IOError:
            print "error reading" , fname

        if i % int(N/10) == 0:
            print "%d/%d images read" % (i,N)


    X = spvq.whiten(X)

    sp.random.seed(20110201)
    
    centers, err = spvq.kmeans(X, K)
    print err

    assignments, err = spvq.vq(X, centers)

    for k in range(K):
        ndx = sp.where(assignments == k)

        f = plot_montage(images, ndx[0])

        fname = '%s_cluster_%d.png' % (directory, k)
        print "saving" , fname

        plt.savefig(fname)

        del(f)
