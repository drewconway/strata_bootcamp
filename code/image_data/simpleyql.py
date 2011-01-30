#!/usr/bin/env python

from urllib import urlencode
from urllib2 import urlopen
import simplejson as json

YQL_PUBLIC = 'http://query.yahooapis.com/v1/public/yql'

def yql_public(query):
    query_str = urlencode({'q': query, 'format': 'json'})

    url = '%s?%s' % (YQL_PUBLIC, query_str)
    print url
    result = urlopen(url)

    return json.load(result)['query']['results']

if __name__=='__main__':

    # get some cat photos
    query = 'select * from flickr.photos.search where text="cat" limit 10'

    print yql_public(query)
