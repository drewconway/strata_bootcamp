#!/usr/bin/env python
# encoding: utf-8
"""
email_timestamps.py

Created by Hilary Mason on 2011-02-01.
Copyright (c) 2011 Hilary Mason. All rights reserved.
"""

import sys, os
from gmail import Gmail

class emailTimestamps(object):

    def __init__(self, username, password):

        e = Gmail(username, password)
        e.select_folder("waiting")
        message_ids = e.get_message_ids()
        self.process_messages(e, message_ids)        
        
    def get_date(self, e, message_ids):
        
        for emailid in message_ids:
            resp, data = e.m.fetch(emailid, "(RFC822)") # fetching the mail, "`(RFC822)`" means "get the whole stuff", but you can ask for headers only, etc
            email_body = data[0][1] # getting the mail content
            mail = email.message_from_string(email_body) # parsing the mail content to get a mail object
            
            # print mail
            for received in mail.get_all("Received"):
                date_string = received.split(';').pop().strip()
                print date_string
        

if __name__ == '__main__':
	e = emailTimestamps("ann9enigma@gmail.com", "stratar0x")

