#!/usr/bin/env python

import sys
import os.path
import scipy as sp
import matplotlib.image as mpimg
import matplotlib.pyplot as plt
import scipy.cluster.vq as spvq
import matplotlib.cm as cm
from mpl_toolkits.mplot3d import Axes3D

if __name__=='__main__':
    if len(sys.argv) == 3:
        # take image filename and number of clusters from command line
        fname = sys.argv[1]
        K = int(sys.argv[2])
    else:
        # default to picture of candy
        fname = 'candy.jpg'

        # number of clusters
        K = 7

        if not os.path.exists(fname):
            # download the image from flickr if missing
            from urllib import urlretrieve
            print "downloading http://www.flickr.com/photos/minebilder/68826730/ to" , fname
            urlretrieve('http://farm1.static.flickr.com/35/68826730_a6556f07cf_s_d.jpg', filename='candy.jpg')


    # read image
    I = mpimg.imread(fname)
    # each pixel is an example, with with (r,g,b) values as the feature vector
    X = sp.reshape(I, (-1,3), order='F')

    # set seed so we all see the same random numbers
    sp.random.seed(20110201)

    # run k-means
    centers, err = spvq.kmeans(X, K)
    # get cluster assignments for each pixel
    assignments, err = spvq.vq(X, centers)
    Z = centers[assignments]

    # begin 3-panel plot

    # plot original image on the left
    plt.subplot(131)
    plt.imshow(I, cmap=cm.gray, interpolation='nearest', origin='lower')


    # NOTE: if you are using a version of matplotlib < 1.0 you will
    # either need to upgrade to the newest version, or use the fix
    # suggested here: http://stackoverflow.com/questions/3810865/need-help-with-matplotlib

    # plot clustered pixels in rgb space in the center
    ax = plt.subplot(132, projection='3d', aspect='equal')
    #ax.view_init(30, 135)
    #colors = assignments
    colors = sp.array(Z, dtype='float') / 255
    ax.scatter(X[:,0], X[:,1], X[:,2], color=colors, alpha=0.25)
    ax.set_xlabel('R')
    ax.set_ylabel('G')
    ax.set_zlabel('B')

    # plot compressed image on the right
    plt.subplot(133)
    Icomp = sp.reshape(Z, I.shape, order='F')
    plt.imshow(Icomp, interpolation='nearest', origin='lower')

    # redraw to fix bug in center panel
    plt.draw()

    # save 3-panel plot
    base, ext = os.path.splitext(fname)
    fname = '%s_clustered.png' % base
    print "saving" , fname
    plt.savefig(fname, bbox_inches='tight')
