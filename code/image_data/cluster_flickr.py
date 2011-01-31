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
    tot_height = 0
    for i in range(N):

        I = sp.array(images[ndx[i]], dtype='float')
        I = I / I.max()
        
        height = I.shape[0]
        width = I.shape[1]
        ax = plt.figimage(I, xo=width*col, yo=height*row, origin='lower')

        col += 1
        if col % ncol == 0:
            row += 1
            col = 0
            tot_height += height

    tot_height += height
    tot_width = width*ncol
    
    f.set_figheight(tot_height/100)
    f.set_figwidth(tot_width/100)

    return f

if __name__=='__main__':

    if len(sys.argv) == 4:
        # take image directory, number of clusters, bins from command line
        directory = sys.argv[1]
        K = int(sys.argv[2])
        bins = int(sys.argv[3])
    else:
        # default to pictures tagged with 'vivid', 3 clusters, 10 bins
        directory = 'flickr_vivid'
        K = 3
        bins = 10
    
    # read images
    images = read_image_dir(directory, '*.jpg')
    N = len(images)

    # generate bag-of-pixels features
    X = sp.zeros( (N,3*bins) )
    for i, image in enumerate(images):
        X[i,:] = rgb_features(image, bins)
    # normalize features
    X = spvq.whiten(X)

    # set seed so we all see the same random numbers
    sp.random.seed(20110201)

    # run k-means
    centers, err = spvq.kmeans(X, K)
    # get cluster assignments for each image
    assignments, err = spvq.vq(X, centers)

    # plot images in each cluster
    for k in range(K):
        # index of images in this cluster
        ndx = sp.where(assignments == k)

        # plot montage
        f = plot_montage(images, ndx[0])

        # save figure
        fname = '%s_cluster_%d.png' % (directory, k)
        print "saving" , fname
        plt.savefig(fname)
        del(f)
