#!/usr/bin/env python
# encoding: utf-8
"""
gmail.py

Created by Hilary Mason on 2011-01-27.
Copyright (c) 2011 Hilary Mason. All rights reserved.
"""

import sys, os
import imaplib

class Gmail(object):
    def __init__(self, email_address, password=''):
        self.m = imaplib.IMAP4_SSL('imap.gmail.com', 993)
        self.m.login(email_address,password)
        self.m.select()
        
    def list_folders(self):
        (status, folder_list) = self.m.list()

        folder_names = []
        for f in folder_list:
            label = f.split('"')[-2] # HACKY: parsing this can get messy
            folder_names.append(label)
            
        return folder_names
        
    def select_folder(self, folder_name=None):
        self.m.select(folder_name)
        
    def get_message_ids(self, folder_name=None):
        if folder_name:
            self.select_folder(folder_name)
        
        try:
            response, items = self.m.search(None, "ALL")        
            items = items[0].split() 
            return items
        except imaplib.IMAP4.error:
            return []
    
    def get_message(self, message_id):
        (resp, data) = self.m.fetch(message_id, "(RFC822)") # fetching the mail, "`(RFC822)`" means "get the whole stuff", but you can ask for headers only, etc
        return data[0][1]
        # email_body = data[0][1] # getting the mail content
        # mail = email.message_from_string(email_body) # parsing the mail content to get a mail object
            
        # # print mail
        # for received in mail.get_all("Received"):
        #     date_string = received.split(';').pop().strip()
        #     # date_string = date_string.split('-')[0].strip()
        #     # message_date = time.strptime(date_string, "%a, %d %b %Y %H:%M:%S")
        #     message_date = email.utils.parsedate(date_string)
        #     time_delta = time.mktime(time.localtime()) - time.mktime(message_date)
        #     if time_delta >= self.nag_seconds:
        #         to_nag.append(mail)
        #     break # one per message
        
        # return to_nag

    # def get_message_headers(self, message_id):
    #     (resp, data) = self.m.fetch(message_id, "(BODY[HEADER.FIELDS (FROM TO CC DATE SUBJECT MESSAGE-ID)])")
        
            
    def create_message(self, to_addr, from_addr, subject='', text=''):
        msg = email.Message.Message()
        msg['To'] = to_addr
        msg['From'] = from_addr
        msg['Subject'] = subject
        
        print email.message_from_string(msg)

if __name__ == '__main__':
    username = 'ann9enigma@gmail.com'
    password = 'stratar0x'

    g = gmail(username, password)
