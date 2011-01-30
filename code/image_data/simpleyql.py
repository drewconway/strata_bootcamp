#!/usr/bin/env python

from urllib import urlencode
from urllib2 import urlopen
import simplejson as json

YQL_PUBLIC = 'http://query.yahooapis.com/v1/public/yql'

def yql_public(query):
    # escape query
    query_str = urlencode({'q': query, 'format': 'json'})

    # fetch results
    url = '%s?%s' % (YQL_PUBLIC, query_str)
    result = urlopen(url)

    # parse json and return
    return json.load(result)['query']['results']

if __name__=='__main__':

    # get some cat photos
    query = 'select * from flickr.photos.search where tags="cat" and sort="interestingness-desc" limit 10'

    # make call to yql
    results = yql_public(query)

    print "some cat photos:"
    for photo in results['photo']:
        print 'http://www.flickr.com/photo.gne?id=%s' % photo['id']
