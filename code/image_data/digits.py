#!/usr/bin/env python

import scipy as sp
import matplotlib.pyplot as plt
import matplotlib.cm as cm
import matplotlib.image as image

# image width
IM_WIDTH=16

def read_digits(dir='digits'):
    """
    read all example digits return a matrix X, where each row is the
    (flattened) pixels of an example digit and a vector y, where each
    entry gives the digit as an integer
    """
    
    for d in range(10):
        fname = '%s/train.%d' % (dir, d)

        print "reading" , fname

        # read digits from train.d
        Xd = sp.loadtxt(fname, delimiter=',')

        # create vector of labels
        yd = d*sp.ones((Xd.shape[0],1))

        try:
            # append digits and labels to X and y, respectively
            X = sp.vstack((X, Xd))
            y = sp.vstack((y, yd))
        except UnboundLocalError:
            # create X and y if they don't exist
            X = Xd
            y = yd
            
    return y, X


def reshape_digit(X, i, width=IM_WIDTH):
    """
    reshape the i-th example (row of X) to a 2d array
    """
    return X[i,:].reshape(-1,width)

def plot_digit(X, i, width=IM_WIDTH):
    """
    plot the i-th example (row of X) as an image
    """

    I = reshape_digit(X, i, width)
    plt.imshow(I, cmap=cm.gray, interpolation='nearest')


def save_digit(X, i, fname, width=IM_WIDTH):
    """
    save the i-th example (row of X) to a file
    """

    plt.imsave(fname, reshape_digit(X, i, width), cmap=cm.gray)

def plot_digits(X, ndx, ncol=50, width=IM_WIDTH, cmap=cm.gray):
    """
    plot a montage of the examples specified in ndx (as rows of X)
    """

    row = 0
    col = 0
    for i in range(ndx.shape[0]):
        
        plt.figimage(reshape_digit(X, ndx[i]),
                     xo=width*col, yo=width*row,
                     origin='upper', cmap=cmap)

        col += 1
        if col % ncol == 0:
            row += 1
            col = 0

            
if __name__=='__main__':

    # read digits
    y, X = read_digits()

    # number of example digits
    N = y.shape[0]

    # save a random digit to sample_digit.png
    sp.random.seed(20110201)
    i = sp.random.randint(N)
    save_digit(X, i, 'sample_digit.png')

    # save a montage of random digits to a sample_digits.png
    ndx = sp.random.randint(0, N, 2000)
    plot_digits(X, ndx)
    plt.savefig('sample_digits.png')

    #plt.show()

