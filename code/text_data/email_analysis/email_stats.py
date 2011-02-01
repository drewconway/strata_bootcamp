#!/usr/bin/env python
# encoding: utf-8
"""
email_stats.py

Created by Hilary Mason on 2011-01-31.
Copyright (c) 2011 Hilary Mason. All rights reserved.
"""

import sys, os
from gmail import Gmail

if __name__ == '__main__':
	g = Gmail("ann9enigma@gmail.com", "stratar0x")
	
	folder_stats = {}
	folder_stats['inbox'] = len(g.get_message_ids())
	
	for folder_name in g.list_folders():
	    folder_stats[folder_name] = len(g.get_message_ids(folder_name))
	    
	for folder_name, count in folder_stats.items():
	    print "Folder %s, # messages: %s" % (folder_name, count)

