#!/usr/bin/env python

from urllib import urlencode
from urllib2 import urlopen
import simplejson as json
import sys

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

    if len(sys.argv) == 2:
        # take yql query from first command line argument
        query = sys.argv[1]
    else:
        # default to pictures of kittens
        query = 'select * from flickr.photos.search where tags="kittens" and sort="interestingness-desc" limit 10'

    print query

    # make call to yql
    results = yql_public(query)

    # pretty-print results
    print json.dumps(results, indent=2)

