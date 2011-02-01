#!/usr/bin/env python
# encoding: utf-8
"""
parse_html.py

Created by Hilary Mason on 2011-01-31.
Copyright (c) 2011 Hilary Mason. All rights reserved.
"""

import sys, os
from BeautifulSoup import BeautifulSoup

def main():
    f = open('bootcamp.html', 'r')     # load file
    contents = f.read()
    f.close()
    
    soup = BeautifulSoup(contents) # parse file
    
    description = soup.find(attrs={'class':'en_session_description description'}) # find node
    
    print description.prettify() #explore
    
    print description.text
    
    
if __name__ == '__main__':
	main()

