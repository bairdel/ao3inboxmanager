import imaplib
import email
from email.header import decode_header
from alive_progress import alive_bar
import sys
import re


def pickFolder(folders, message):
    for i in range(len(folders)):
        folders[i] = folders[i].decode('utf-8').split('"')[-2]
        print(str(i + 1) + ": " + str(folders[i]))
    ind = int(input("\n" + message + ": ")) - 1
    return '"' + str(folders[ind]) + '"'

def sortCompletedFics(username, password):

    ## https://thepythoncode.com/article/reading-emails-in-python

    imap_server = "imap.mail.yahoo.com"
    # create an IMAP4 class with SSL 
    imap = imaplib.IMAP4_SSL(imap_server)

    # print(username)
    # print(password)
    # authenticate
    imap.login(username, password)

    ######## manual options

    # inbox = pickFolder(imap.list()[1], "Which folder to sort?")
    # status, messages = imap.select(mailbox=(inbox))
    # destinationFolder = pickFolder(imap.list()[1], "Which folder to go into?")

    # print(inbox + " finished fics into " + destinationFolder)

    # # total number of emails
    # messages = int(messages[0])
    # # number of top emails to fetch
    # N = messages



    inboxMovements = [['"Avatar the Last Airbender"','"Avatar the Last Airbender/ATLA finished"'],
                        ['"Avatar the Last Airbender/ATLA WIPs"','"Avatar the Last Airbender/ATLA finished"'],
                        ['"Star Wars"','"Star Wars/Star Wars Finished"'],
                        ['"Star Wars/Star Wars WIPs"','"Star Wars/Star Wars Finished"'],
                        ['"The Murderbot Diaries"','"The Murderbot Diaries/The Murderbot Diaries Finished"'],
                        ['"Percy Jackson/PJO WIPs"','"Percy Jackson"'],
                        ['"Miraculous Ladybug"','"Miraculous Ladybug/Miraculous Finished"'],
                        ['"Miraculous Ladybug/Miraculous WIPs"','"Miraculous Ladybug/Miraculous Finished"'],
                        ['"Harry Potter/Harry Potter WIPs"','"Harry Potter"'],
                        ['"BNHA/Midoriya Izuku"','"BNHA/Midoriya Izuku Finished"'],
                        ['"BNHA WIPs/Midoriya Izuku WIPs"','"BNHA/Midoriya Izuku Finished"'],
                        ['"Merlin/Merlin WIPs"','"Merlin"'],
                        ['"The Untamed"','"The Untamed/The Untamed Finished"'],
                        ['"The Untamed/Untamed WIPs"','"The Untamed/The Untamed Finished"'],
                        ['"Others"','"Others/Others Finished"'],
                        ['"DC/Jason Todd, Tim Drake"','"DC/JTTD Finished"'],
                        ['"Marvel"','"Marvel/Marvel Finished"'],
                        ['"Marvel/Marvel WIPs"','"Marvel/Marvel Finished"'],
                        ['"DSMP"','"DSMP/DSMP Finished"'],
                        ['"DSMP/DSMP WIPs"','"DSMP/DSMP Finished"'],
                        ['"Good Omens"','"Good Omens/Good Omens Finished"'],
                        ['"Danny Phantom"','"Danny Phantom/Danny Phantom Finished"']]
    
    longfics = [['"Star Wars/Star Wars Finished"', '"Star Wars/Star Wars Long"'],
                ['"The Untamed/The Untamed Finished"', '"The Untamed/The Untamed Long"'],
                ['"DC/JTTD Finished"', '"DC/DC Long"'],
                ['"BNHA/Midoriya Izuku Finished"','"BNHA/BNHA Finished Long"'],
                ['"Miraculous Ladybug/Miraculous Finished"', '"Miraculous Ladybug/Miraculous Longfics"'],
                ['"Danny Phantom/Danny Phantom Finished"', '"Danny Phantom/Danny Phantom Long"'],
                ['"Avatar the Last Airbender/ATLA finished"', '"Avatar the Last Airbender/ATLA Long"']]
    
    # inboxMovements = [['"DSMP/DSMP WIPs"','"DSMP/DSMP Finished"']]
    

    for k in range(len(longfics)):
        inbox = longfics[k][0]
        status, messages = imap.select(mailbox=(inbox))

        destinationFolder = longfics[k][1]


    # total number of emails
        messages = int(messages[0])

        # number of top emails to fetch
        if messages < 400:
            N = messages
        else:
            N = 400

        with alive_bar(N, title=(inbox + " finished fics into " + destinationFolder)) as bar:
            for i in range(messages, messages-N, -1):


                # fetch the email message by ID
                res, msg = imap.fetch(str(i), "BODY.PEEK[]")
                for response in msg:
                    if isinstance(response, tuple):
                        uid = response[0].decode('utf-8')
                        uid = uid.split("UID ")[1].split(" BODY")[0]
                        # print(uid)
                        # parse a bytes email into a message object
                        msg = email.message_from_bytes(response[1])
                        # decode the email subject
                        subject, encoding = decode_header(msg["Subject"])[0]
                        if isinstance(subject, bytes):
                            # if it's a bytes, decode to str
                            subject = subject.decode(encoding)
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
                                            # print(body.split("Chapters: ")[1].split("\nFandom:")[0])
                                            chapters = (body.split("Chapters: ")[1].split("\nFandom:")[0]).strip(" ").strip("\r").split("/")
                                            words = re.findall(r"\((\d*?) words\)", body)
                                            # print(words)
                                                # print("Complete")
                                            if int(words[0]) > 20000:
                                                #longfic

                                                imap.uid('MOVE', uid ,destinationFolder)
                                                print("words " + words[0] + " moved to " + destinationFolder)

                                                bar.text = subject

                                            else:
                                                # print("incomplete")
                                                pass
                                        except Exception as e:
                                            print(e)
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


# if __name__ == "__main__":
#     from keys import username, password
#     sortCompletedFics(username, password)
    

sortCompletedFics(sys.argv[1], sys.argv[2])
