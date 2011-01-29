 # File-Name:       company_similarity.R           
# Date:            2011-01-27                                
# Author:          Drew Conway
# Email:           drew.conway@nyu.edu                                      
# Purpose:         Cluster companies at the tutorial based on attendee position
# Data Used:       StrataBootcamp_Roster.csv
# Packages Used:   tm, ggplot2
# Output File:     
# Data Output:     
# Machine:         Drew Conway's MacBook Pro

# Copyright (c) 2011, under the Simplified BSD License.  
# For more information on FreeBSD see: http://www.opensource.org/licenses/bsd-license.php
# All rights reserved.                                                         

# Load libraries and data
library(ggplot2)
library(tm)
library(igraph)

attendee.df<-read.csv("../../data/StrataBootcamp_Roster.csv",stringsAsFactors=FALSE)

# Create corpus from data frame
position.text<-PlainTextDocument(attendee.df$user.position)
attendee.corpus<-Corpus(DataframeSource(attendee.df))

# Get term frequencies for positions
position.control=list(stopwords=c(stopwords()), removeNumbers=TRUE, removePunctuation=TRUE)
position.freq<-termFreq(position.text, control=position.control)

# Create a Term-Document matrix
affiliation.control=list(stopwords=c(stopwords()), removePunctuation=TRUE)
attendee.matrix<-TermDocumentMatrix(attendee.corpus, control=affiliation.control)

# Find associated terms from user affilaitions
position.assocs<-sapply(names(position.freq[which(position.freq>1)]), function(t) findAssocs(attendee.matrix,t,0.2))

# Create data frame from term correlation
assocs.columns<-sapply(position.assocs, function(x) cbind(names(x),names(x[which(x==1)]),x))
assocs.df<-do.call(rbind, lapply(assocs.columns, data.frame, stringsAsFactors=FALSE))

# Clean up names and re-set types
row.names(assocs.df)<-1:nrow(assocs.df)
names(assocs.df)<-c("Company", "Position", "Corr")
assocs.df$Corr<-as.numeric(assocs.df$Corr)

# Extract position types from Company column
assocs.final<-assocs.df[is.na(match(assocs.df$Company,unique(assocs.df$Position))),]

# Create a weighted igraph object from the data frame
databootcamp.graph<-graph.data.frame(assocs.final)

# Create a type vector for visualization, and add it
graph.type<-is.bipartite(databootcamp.graph)$type
graph.type<-ifelse(graph.type,"Position","Company")
databootcamp.graph<-set.vertex.attribute(databootcamp.graph,name="Type",value=graph.type)

# Set the name labels
databootcamp.graph<-set.vertex.attribute(databootcamp.graph,name="Label",value=V(databootcamp.graph)$name)

# Finally, export graph
write.graph(databootcamp.graph, "../../data/databootcamp_graph.graphml",format="graphml")
