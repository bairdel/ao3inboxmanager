import imaplib
import email
from email.header import decode_header
from keys import username, password
from alive_progress import alive_bar


def pickFolder(folders, message):
    for i in range(len(folders)):
        folders[i] = folders[i].decode('utf-8').split('"')[-2]
        print(str(i + 1) + ": " + str(folders[i]))
    ind = int(input("\n" + message + ": ")) - 1
    return '"' + str(folders[ind]) + '"'

def detailedSearch(username, password):

    ## https://thepythoncode.com/article/reading-emails-in-python

    imap_server = "imap.mail.yahoo.com"
    # create an IMAP4 class with SSL 
    imap = imaplib.IMAP4_SSL(imap_server)
    # authenticate
    imap.login(username, password)

    inbox = pickFolder(imap.list()[1], "Which folder to search?")
    status, messages = imap.select(mailbox=(inbox))
    destinationFolder = pickFolder(imap.list()[1], "Which folder to go into?")

    searchTerm = input("Term to search for: ")
    # searchTerm = "Bakugou Katsuki/Midoriya Izuku"

    messages = int(messages[0])
    # number of top emails to fetch
    N = messages
    # N = 15


    with alive_bar(N, title=(inbox + " finished fics into " + destinationFolder)) as bar:
        for i in range(messages, messages-N, -1):


            # fetch the email message by ID
            res, msg = imap.fetch(str(i), "BODY.PEEK[]")
            for response in msg:
                if isinstance(response, tuple):
                    uid = response[0].decode('utf-8')
                    uid = uid.split("UID ")[1].split(" BODY")[0]
                    # parse a bytes email into a message object
                    msg = email.message_from_bytes(response[1])
                    # decode the email subject
                    subject, encoding = decode_header(msg["Subject"])[0]
                    if isinstance(subject, bytes):
                        # if it's a bytes, decode to str
                        subject = subject.decode(encoding)
                        bar.text = subject
                    # decode email sender
                    From, encoding = decode_header(msg.get("From"))[0]
                    if isinstance(From, bytes):
                        From = From.decode(encoding)
                    # print("Subject:", subject)
                    # print("From:", From)
                    # if the email message is multipart
                    if From == "Archive of Our Own <do-not-reply@archiveofourown.org>":
                        if msg.is_multipart():
                            # iterate over email parts
                            for part in msg.walk():
                                # extract content type of email
                                content_type = part.get_content_type()
                                content_disposition = str(part.get("Content-Disposition"))
                                try:
                                    # get the email body
                                    body = part.get_payload(decode=True).decode()
                                except:
                                    pass
                                if content_type == "text/plain" and "attachment" not in content_disposition:
                                    # print text/plain emails and skip attachments
                                    try:
                                        # print(subject)
                                        if searchTerm in body:
                                            imap.uid('MOVE', uid ,destinationFolder)
                                            print(subject)

                                        
                                    except:
                                        print(body)
                                        pass
                        else:
                            # extract content type of email
                            content_type = msg.get_content_type()
                            # get the email body
                            body = msg.get_payload(decode=True).decode()
                            if content_type == "text/plain":
                                # print only text email parts
                                print(body)

                    bar()

    # close the connection and logout
    imap.close()
    imap.logout()


if __name__ == "__main__":
    detailedSearch(username, password)