import imaplib
import email
from email.header import decode_header
from alive_progress import alive_bar
import sys
import re
from keys import username, password

def listFolders(username, password):

    ## https://thepythoncode.com/article/reading-emails-in-python

    imap_server = "imap.mail.yahoo.com"
    # create an IMAP4 class with SSL 
    imap = imaplib.IMAP4_SSL(imap_server)

    # print(username)
    # print(password)
    # authenticate
    imap.login(username, password)

    ######## manual options
    folders = imap.list()[1]
    for i in range(len(folders)):
        folders[i] = folders[i].decode('utf-8').split('"')[-2]
        print(str(i + 1) + ": " + str(folders[i]))

    # imap.close()
    imap.logout()


listFolders(username, password)
# listFolders(sys.argv[1], sys.argv[2])
