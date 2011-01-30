#!/usr/bin/env python
# encoding: utf-8
"""
email_edges.py

Created by Hilary Mason on 2011-01-29.
Copyright (c) 2011 Hilary Mason. All rights reserved.
"""

import sys, os
import csv
from gmail import Gmail

class email_edges(object):

    def __init__(self, username, password):
        g = Gmail(username, password)
        
        graph_out = csv.writer(open('email_graph.csv', 'wb'))
        
        viewed_messages = []
        for folder in g.list_folders(): # iterate through all folders in the account
            # print "%s: %s" % (folder, g.get_message_ids(folder)) # NOTE: uncomment this to see which ids are in each folder
            for message_id in g.get_message_ids(folder): # iterate through message IDs
                if message_id not in viewed_messages: # ...but don't repeat messages
                    # print "Processing %s" % message_id
                    msg = g.get_message(message_id)
                    
                    for line in msg.split('\n'): # grab the from and to lines
                        line = line.strip()
                        if line[0:5] == "From:":
                            msg_from = line[5:].strip()
                        elif line[0:3] == "To:":
                            msg_to = line[3:].strip()
                        
                    try:
                        # print "%s, %s" % (msg_from, msg_to) # DEBUG
                        graph_out.writerow([msg_from, msg_to]) # output the from and to
                    except UnboundLocalError: # ignore if we can't read the headers
                        pass
                        
        

if __name__ == '__main__':
    try:
        filename = sys.argv[1]
    except IndexError:
        filename = "email_graph.csv"
        
    username = 'ann9enigma@gmail.com'
    password = 'stratar0x'
	
    e = email_edges(username, password)

