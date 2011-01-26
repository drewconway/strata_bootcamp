#!/usr/bin/env python
# encoding: utf-8
"""
first_viz.py

Purpose:  Creating a first matplotlib visualization
            (Strata - Data Bootcamp Tutorial)
Author:   Drew Conway
Email:    drew.conway@nyu.edu
Date:     2011-01-25

Copyright (c) 2011, under the Simplified BSD License.  
For more information on FreeBSD see: http://www.opensource.org/licenses/bsd-license.php
All rights reserved.
"""

import sys
import os
import matplotlib.pylab as plt
from scipy.stats import norm

def plot_normal(random_numbers, path=""):
    """
    A function to graphically check a random distribution's
    fit to a theoretical normal.
    """
    fig=plt.figure(figsize = (8,6)) # Create a figure to plot in (good habit)
    # Histogram of random numbers with 25 bins
    n, bins, pataches = plt.hist(random_numbers,normed=True,bins=25,alpha=0.75)  
    # Add "best fit" line
    y = norm.pdf(bins)
    plt.plot(bins,y,"r-")
    # Save plot
    plt.xlabel("Random numbers")
    plt.ylabel("Density")
    plt.title("My first matplotlib visualization!")
    plt.savefig(path)

def main():
    random_normal = norm.rvs(0,1,size=10000)
    plot_normal(random_normal,"../../../images/figures/matplotlib_first.png")

if __name__ == '__main__':
	main()

