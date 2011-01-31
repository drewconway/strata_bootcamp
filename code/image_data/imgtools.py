#!/usr/bin/env python

import scipy as sp
import matplotlib.image as mpimg
import matplotlib.pyplot as plt
import sys
import os.path
import glob

def rgb_hist(I, ax, bins=256):

    # run over red, green, and blue channels
    channels = ('r','g','b')
    for i, color in enumerate(channels):
        # get count pixel intensities for this channel
        counts, bins, patches = plt.hist(I[:,:,i].flatten(), bins=bins, normed=True, visible=False)

        # hack: choose mid-point of bins as centers
        centers = bins[:-1] + sp.diff(bins)/2

        # line plot with fill
        plt.plot(centers, counts, color=color)
        ax.fill_between(centers, 0, counts, color=color, alpha=0.25)

    # hack for matlab's axes('square') function
    # http://www.mail-archive.com/matplotlib-users@lists.sourceforge.net/msg08388.html
    plt.axis('tight')
    ax.set_aspect(1./ax.get_data_ratio())


def imshow_hist(I, bins=256):

    f = plt.figure()

    # show image in left panel
    plt.subplot(121)
    plt.imshow(I, origin='lower')

    # show histogram in right panel
    ax = plt.subplot(122)
    rgb_hist(I, ax, bins)

    return f


def rgb_features(I, bins=10):

    x = sp.array([])

    # run over red, green, and blue channels
    channels = ('r','g','b')
    for i, color in enumerate(channels):
        # get count pixel intensities for this channel
        counts, bins = sp.histogram(I[:,:,i].flatten(), bins=bins)

        x = sp.concatenate( (x, counts) )

    return x


def read_image_dir(directory, pattern='*.jpg'):
    # glob for image files
    fnames = glob.glob('%s/%s' % (directory, pattern))
    N = len(fnames)

    # read images 
    print "reading %d image files from %s" % (N, directory)
    images = []
    for i, fname in enumerate(fnames):
        try:
            I = mpimg.imread(fname)
            images.append(I)            
        except IOError:
            print "error reading" , fname

        # show progress
        if i % int(N/10) == 0:
            print "%d/%d images read" % (i,N)

    return images


if __name__=='__main__':

    if len(sys.argv) == 3:
        # take image filename and number of bins from command line
        fname = sys.argv[1]
        bins = int(sys.argv[2])
    else:
        # default to picture of chairs
        fname = 'chairs.jpg'
        bins = 64

        # download the image from flickr if missing
        if not os.path.exists(fname):
            from urllib import urlretrieve
            print "downloading http://www.flickr.com/photos/dcdead/4871475924/ to" , fname
            urlretrieve('http://farm5.static.flickr.com/4097/4871475924_dcc135dd8f_b_d.jpg', filename='chairs.jpg')

    # load the image
    I = mpimg.imread(fname)

    # display with a histogram
    imshow_hist(I, bins)

    # save figure
    base, ext = os.path.splitext(fname)
    fname = '%s_%d.png' % (base, bins)
    print "saving" , fname
    plt.savefig(fname)
