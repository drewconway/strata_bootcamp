# File-Name:       first_viz.R           
# Date:            2011-01-25                                
# Author:          Drew Conway
# Email:           drew.conway@nyu.edu                                      
# Purpose:         Creating a first matplotlib visualization
#                   (Strata - Data Bootcamp Tutorial)
# Data Used:       
# Packages Used:   ggplot2
# Output File:     ggplot2_first.png
# Data Output:     
# Machine:         Drew Conway's MacBook Pro

# Copyright (c) 2011, under the Simplified BSD License.  
# For more information on FreeBSD see: http://www.opensource.org/licenses/bsd-license.php
# All rights reserved.                                                         

# Load libraries
library(ggplot2)

# Generate random numbers and create data frame
random.numbers <- rnorm(10000,0,1)
norm.dframe <- as.data.frame(list(Norm=random.numbers))

# Build graphical layers
norm.plt <- ggplot(norm.dframe,aes(Norm))+ # The first layer is the ggplot2 object, and a data frame
    geom_histogram(aes(y = ..density.., fill="blue", colour="black",alpha=0.75))+    # Build a histogram
    stat_function(fun = dnorm, colour = "red")+     # Overlay the normal density function
    scale_colour_manual(values = c("black"="black","red"="red"), legend = FALSE)+   # Do housekeeping on colors
    scale_fill_manual(values = c("blue"="blue"), legend = FALSE)+
    scale_alpha(legend = FALSE)+
    xlab("Random numbers")+ylab("Density")+     # Add labels
    opts(title="My first ggplot2 visualization!")
    
# Save plot
ggsave(plot = norm.plt, filename = "../../../images/figures/ggplot2_first.pdf", height = 6, width = 8)