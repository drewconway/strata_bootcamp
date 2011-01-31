#!/usr/bin/env python

from simpleyql import *
import simplejson as json
from urllib import urlretrieve
import os

def photo_url(photo, size='s'):
    url = "http://farm%s.static.flickr.com/%s/%s_%s_%s.jpg" % (photo['farm'],
                                                               photo['server'],
                                                               photo['id'],
                                                               photo['secret'],
                                                               size)    
    return url

if __name__=='__main__':
    # default to 500 pictures tagged with 'vivid'
    tags = 'vivid'
    n = 500
    offset = 0
    
    # take tags, number of images, and offset from command line
    try:
        tags = sys.argv[1]
        n = int(sys.argv[2])
        offset = int(sys.argv[3])
    except:
        pass

    # grab the top-n most interesting photos tagged with 'tags'
    query = '''select * from flickr.photos.search(%d,%d) where
    tags="%s" and sort="interestingness-desc"
    ''' % (offset, n, tags)

    # make yql call
    print "fetching %d photos tagged with %s from flickr" % (n, tags)
    results = yql_public(query)

    # create output directory if it doesn't exist
    directory = 'flickr_%s' % tags
    if not os.path.exists(directory):
        print "creating directory %s" % directory
        os.mkdir(directory)

    # run over results
    for photo in results['photo']:
        # build url of square image
        square_url = photo_url(photo)

        # download square image
        fname = '%s/%s.jpg' % (directory, photo['id'])
        if not os.path.exists(fname):
            print square_url , "->" , fname
            urlretrieve(square_url, filename=fname)
