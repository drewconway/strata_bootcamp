# File-Name:       twitter_word_cloud.R           
# Date:            2011-01-30                                
# Author:          Drew Conway
# Email:           drew.conway@nyu.edu                                      
# Purpose:         Create a comparative word cloud of two twitter hashtags
# Data Used:       
# Packages Used:   twitteR, tm, ggplot2
# Output File:     Hashtag word cloud
# Data Output:     
# Machine:         Drew Conway's MacBook Pro

# Copyright (c) 2011, under the Simplified BSD License.  
# For more information on FreeBSD see: http://www.opensource.org/licenses/bsd-license.php
# All rights reserved.                                                         

# This function takes two twitter hash-tags and creates a comparatice hash-tag as first
# introduced here: http://www.drewconway.com/zia/?p=2624
comparative.wordcloud<-function(hashtag1, hashtag2, file.path, n=100, add.stops=c()) {
    ### Parameters ###
    # hashtag1:     First Twitter hashtag to search for (do not include '#' or spaces)
    # hashtag2:     Second Twitter hashtag to search for (do not include '#' or spaces)
    # file.path:    File path for saving word cloud (uses ggsave, so file type must be supported)
    #               by ggplot2.  For file types see ?ggsave
    # n:            The number of tweets to download for each hashtag (default is 100)
    # add.stops:    Addional stopwords to purge from corpuses
    
    # This supplemental function takes some number as spaces and returns a vertor
    # of continuous values for even spacing centered around zero.  It is used to 
    # minimze over-plotting on the y-axis, and maxmize the readability of the plot.
    optimal.spacing<-function(spaces) {
        if(spaces>1) {
            spacing<-1/spaces
            if(spaces%%2 > 0) {
                lim<-spacing*floor(spaces/2)
                return(seq(-lim,lim,spacing))
            }
            else {
                lim<-spacing*(spaces-1)
                return(seq(-lim,lim,spacing*2))
            }
        }
        else {
            return(0)
        }
    }
    
    ### 0) First check for all required packages, and load
    if (!require(twitteR)) install.packages('twitteR', dependencies=TRUE)
    library(twitteR)
    if (!require(tm)) install.packages('tm', dependencies=TRUE)
    library(tm)
    if (!require(ggplot2)) install.packages('ggplot2', dependencies=TRUE)
    library(ggplot2)
    
    ### 1) Download recent tweets with each hashtag and create text Corpus 
    #   with separate documents for text mine from each hashtag
    hashtag1<-gsub("[# ]","",hashtag1)  # Strip out the '#' and spaces to
    hashtag2<-gsub("[# ]","",hashtag2)  # make searching work properly
    
    hash1.search<-searchTwitter(paste("#",hashtag1,sep=""),n=n)
    hash2.search<-searchTwitter(paste("#",hashtag2,sep=""),n=n)
    
    # Check that the search returned some results
    if(class(hash1.search[[1]])!="status") {
        warning(paste("No search results returned for: ",hashtag1,sep=""))
        stop()
    }
    else {
        if(class(hash2.search[[1]])!="status") {
            warning(paste("No search results returned for: ",hashtag2,sep=""))
            stop()
        }
    }
    cat("Tweets downloaded\n")
    
    hash1.text<-unique(sapply(hash1.search, statusText))    # Due to retweeting
    hash2.text<-unique(sapply(hash2.search, statusText))    # we strip repeats
    
    # Combine texts into a single vector and create a corpus
    text.vec<-c(paste(hash1.text, collapse=" "), paste(hash2.text, collapse=" "))
    hash.corpus<-Corpus(VectorSource(text.vec))
    
    ### 2) Clean data, create Term-Document matrix, and covert to data frame
    add.stops<-c(add.stops,"RT", hashtag1, hashtag2)
    hash.control=list(stopwords=c(stopwords(), add.stops), removeNumbers=TRUE, removePunctuation=TRUE)
    hash.matrix<-TermDocumentMatrix(hash.corpus, control=hash.control)
    
    # Create data frame from matrix
    hash.df<-as.data.frame(inspect(hash.matrix))
    names(hash.df)<-c("hash1.freq", "hash2.freq")
    hash.df<-subset(hash.df, hash1.freq>0 & hash2.freq>0)
    hash.df<-transform(hash.df, freq.dif=hash1.freq-hash2.freq)
    
    ### 3) Set up data for visualization
    # Create separate data frames for each frequency type
    hash1.df<-subset(hash.df, freq.dif>0)   # Said more often in first hashtag
    hash2.df<-subset(hash.df, freq.dif<0)   # Said more often in second hashtag
    equal.df<-subset(hash.df, freq.dif==0)  # Said equally

    # Check that there is some overlap
    if(nrow(hash1.df) < 1 | nrow(hash2.df) < 1) {
        warning("These two hashtags are too dissimialr, there would be no data to plot :(")
        stop()
    }
    
    # Get spacing for each frequency type
    hash1.spacing<-sapply(table(hash1.df$freq.dif), function(x) optimal.spacing(x))
    hash2.spacing<-sapply(table(hash2.df$freq.dif), function(x) optimal.spacing(x))
    equal.spacing<-sapply(table(equal.df$freq.dif), function(x) optimal.spacing(x))
    
    # Add spacing to data frames
    hash1.optim<-rep(0,nrow(hash1.df))
    for(n in names(hash1.spacing)) {
        hash1.optim[which(hash1.df$freq.dif==as.numeric(n))]<-hash1.spacing[[n]]
    }
    hash1.df<-transform(hash1.df, Spacing=hash1.optim, Term=row.names(hash1.df))

    hash2.optim<-rep(0,nrow(hash2.df))
    for(n in names(hash2.spacing)) {
        hash2.optim[which(hash2.df$freq.dif==as.numeric(n))]<-hash2.spacing[[n]]
    }
    hash2.df<-transform(hash2.df, Spacing=hash2.optim, Term=row.names(hash2.df))

    equal.df<-transform(equal.df, Spacing=as.vector(equal.spacing), Term=row.names(equal.df))
    
    ### 4) Create visualization with ggplot2
    # Setup x-axis scaling and labels
    x.break.min<-min(hash2.df$freq.dif)
    x.break.max<-max(hash1.df$freq.dif)
    x.min<-x.break.min-(.1*(min(hash1.df$freq.dif)))
    x.max<-x.break.max+(.1*(max(hash1.df$freq.dif)))
    x.labs<-c(paste("Tweeted more in #",hashtag2,sep=""),"Tweeted equally",paste("Tweeted more in #",hashtag1,sep=""))
    
    # Create ggplot2 object and save plot
    word.cloud<-ggplot(hash1.df, aes(x=freq.dif, y=Spacing))+geom_text(aes(size=hash1.freq, label=Term, colour=freq.dif))+
        geom_text(data=hash2.df, aes(x=freq.dif, y=Spacing, label=Term, size=hash2.freq, color=freq.dif))+
        geom_text(data=equal.df, aes(x=freq.dif, y=Spacing, label=Term, size=hash1.freq, color=freq.dif))+
        scale_size(to=c(3,11), name="Word Frequency")+scale_colour_gradient(low="darkred", high="darkblue", legend=FALSE)+
        scale_x_continuous(limits=c(x.min,x.max),breaks=c(x.break.min,0,x.break.max),labels=x.labs)+
        scale_y_continuous(breaks=c(0),labels=c(""))+xlab("")+ylab("")+theme_bw()+
        opts(panel.grid.major=theme_blank(),panel.grid.minor=theme_blank(), title=paste("Twitter Hashtag Word Cloud 2.0: #",hashtag1," vs. #",hashtag2,sep=""))
    ggsave(plot=word.cloud,filename=file.path,width=15,height=9)
    cat(paste("Word cloud saved to:",file.path,"\n"))
    
    # Return data in list
    return(hash.df)
}

# Example with strataconf and 
ht1<-"strataconf"   # Hash tags to compare
ht2<-"rstats"

hash.data<-comparative.wordcloud(ht1, ht2, paste(ht1,"_",ht2,".png",sep=""), n=100)
