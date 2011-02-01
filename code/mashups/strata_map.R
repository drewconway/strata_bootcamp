# File-Name:       strata_map.R           
# Date:            2011-01-31                                
# Author:          Drew Conway
# Email:           drew.conway@nyu.edu                                      
# Purpose:         Create a map of bit.ly clicks on Strata
# Data Used:       strata_lat_lon
# Packages Used:   ggplot2
# Output File:    
# Data Output:     
# Machine:         Drew Conway's MacBook Pro

# Copyright (c) 2011, under the Simplified BSD License.  
# For more information on FreeBSD see: http://www.opensource.org/licenses/bsd-license.php
# All rights reserved.                                                         

# Load libraries and data
library(ggplot2)
library(maps)

strata.clicks<-read.csv("../../data/strata_lat_lon", header=FALSE, col.names=c("lat","lon"))

# Create a frequnecy count of each lat-lon combo
click.counts<-ddply(strata.clicks,.(lat,lon), "nrow")


# Get map of the world
world.map<-data.frame(map(plot=FALSE)[c("x","y")])

# Plot map
click.plot<-ggplot(world.map, aes(x=x,y=y))+geom_path(aes(colour="grey"))

# Add click points to map
click.plot<-click.plot+geom_point(data=click.counts, aes(x=lon, y=lat, color="red", alpha=0.65, size=nrow))+
    scale_colour_manual(values=c("grey"="grey","red"="red"),legend=FALSE)+scale_alpha(legend=FALSE)+
    coord_map(projection="lagrange",ylim=c(-40,70),xlim=c(-145,155))+theme_bw()+
    opts(panel.grid.major=theme_blank(),axis.ticks=theme_blank(),axis.text.x=theme_blank(),axis.text.y=theme_blank())+
    xlab("")+ylab("")
ggsave(plot=click.plot, filename="strata_map.png", width=11, height=7)