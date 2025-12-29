import imaplib
import email
from email.header import decode_header
from alive_progress import alive_bar
import sys
import re
import regex
# from keys import username, password

debug = False
numMessages = 50


def pickFolder(folders, message):
    for i in range(len(folders)):
        folders[i] = folders[i].decode('utf-8').split('"')[-2]
        print(str(i + 1) + ": " + str(folders[i]))
    ind = int(input("\n" + message + ": ")) - 1
    return '"' + str(folders[ind]) + '"'





    # inboxMovements = [
    #     ['"Avatar the Last Airbender"','"Avatar the Last Airbender/ATLA 3K"'],
    #                     ['"Avatar the Last Airbender/ATLA WIPs"','"Avatar the Last Airbender/ATLA 3K"'],
    #                     ['"Star Wars"','"Star Wars/Star Wars 3K"'],
    #                     ['"Star Wars/Star Wars WIPs"','"Star Wars/Star Wars 3K"'],
    #                     ['"The Murderbot Diaries"','"The Murderbot Diaries/The Murderbot Diaries 3K"'],
    #                     ['"Percy Jackson/PJO WIPs"','"Percy Jackson"'],
    #                     ['"Miraculous Ladybug"','"Miraculous Ladybug/Miraculous 3K"'],
    #                     ['"Miraculous Ladybug/Miraculous WIPs"','"Miraculous Ladybug/Miraculous 3K"'],
    #                     ['"Harry Potter/Harry Potter WIPs"','"Harry Potter/HP 3K"'],
    #                     ['"Harry Potter"','"Harry Potter/HP 3K"'],
    #                     ['"BNHA/Midoriya Izuku"','"BNHA/Midoriya Izuku 3K"'],
    #                     ['"BNHA/Midoriya Izuku WIPs"','"BNHA/Midoriya Izuku 3K"'],
    #                     ['"BNHA"','"BNHA/BNHA 3K"'],
    #                     ['"BNHA/BNHA WIPs"','"BNHA/BNHA 3K"'],
    #                     ['"Merlin/Merlin WIPs"','"Merlin"'],
    #                     ['"The Untamed"','"The Untamed/The Untamed 3K"'],
    #                     ['"The Untamed/Untamed WIPs"','"The Untamed/The Untamed 3K"'],
    #                     ['"Others"','"Others/Others 3K"'],
    #                     ['"DC/Jason Todd, Tim Drake"','"DC/JTTD 3K"'],
    #                     ['"DC/DC WIPs"','"DC/DC 3K"'],
    #                     ['"DC"','"DC/DC 3K"'],
    #                     ['"Marvel"','"Marvel/Marvel 3K"'],
    #                     ['"Marvel/Marvel WIPs"','"Marvel/Marvel 3K"'],
    #                     ['"DSMP"','"DSMP/DSMP 3K"'],
    #                     ['"DSMP/DSMP WIPs"','"DSMP/DSMP 3K"'],
    #                     ['"Good Omens"','"Good Omens/Good Omens 3K"'],
    #                     ['"Danny Phantom"','"Danny Phantom/Danny Phantom 3K"']]
    
    # longfics = [['"Star Wars/Star Wars 3K"', '"Star Wars/Star Wars 20K"'],
    #             ['"The Untamed/The Untamed 3K"', '"The Untamed/The Untamed 20K"'],
    #             ['"DC/JTTD 3K"', '"DC/DC 20K"'],
    #             ['"DC/DC 3K"', '"DC/DC 20K"'],
    #             ['"BNHA/Midoriya Izuku 3K"','"BNHA/BNHA 20K"'],
    #             ['"BNHA/BNHA 3K"','"BNHA/BNHA 20K"'],
    #             ['"Miraculous Ladybug/Miraculous 3K"', '"Miraculous Ladybug/Miraculous 20K"'],
    #             ['"Danny Phantom/Danny Phantom 3K"', '"Danny Phantom/Danny Phantom 20K"'],
    #             ['"Avatar the Last Airbender/ATLA 3K"', '"Avatar the Last Airbender/ATLA 20K"'],
    #             ['"Harry Potter/HP 3K"','"Harry Potter/HP 20K"'],
    #             ['"The Murderbot Diaries/The Murderbot Diaries 3K"','"The Murderbot Diaries/The Murderbot Diaries 20K"'],
    #             ['"Danny Phantom/Danny Phantom 3K"','"Danny Phantom/Danny Phantom 20K"'],
    #             ['"Good Omens/Good Omens 3K"','"Good Omens/Good Omens 20K"'],
    #             ['"Marvel/Marvel 3K"','"Marvel/Marvel 20K"']]
        
    # inboxMovements = [['"DC/Jason Todd, Tim Drake"','"DC/JTTD Finished"']]
    
inboxes = [{'base': '"Avatar the Last Airbender"', 'wips': '"Avatar the Last Airbender/ATLA WIPs"', '3k': '"Avatar the Last Airbender/ATLA 3K"', '20k':'"Avatar the Last Airbender/ATLA 20K"'},
            {'base': '"BNHA/Midoriya Izuku"', 'wips': '"BNHA/Midoriya Izuku WIPs"', '3k': '"BNHA/Midoriya Izuku 3K"', '20k':'"BNHA/BNHA 20K"'},
            {'base': '"Danny Phantom"', 'wips': '"Danny Phantom"', '3k': '"Danny Phantom/Danny Phantom 3K"', '20k':'"Danny Phantom/Danny Phantom 20K"'},
            {'base': '"DC/Jason Todd, Tim Drake"', 'wips': '"DC/Jason Todd, Tim Drake"', '3k': '"DC/JTTD 3K"', '20k':'"DC/DC 20K"'},
            {'base': '"DSMP"', 'wips': '"DSMP/DSMP WIPs"', '3k': '"DSMP/DSMP 3K"', '20k':'"DSMP/DSMP 3K"'},
            {'base': '"Good Omens"', 'wips': '"Good Omens"', '3k': '"Good Omens/Good Omens 3K"', '20k':'"Good Omens/Good Omens 20K"'},
            {'base': '"Harry Potter"', 'wips': '"Harry Potter/Harry Potter WIPs"', '3k': '"Harry Potter/HP 3K"', '20k':'"Harry Potter/HP 20K"'},
            {'base': '"Marvel"', 'wips': '"Marvel/Marvel WIPs"', '3k': '"Marvel/Marvel 3K"', '20k':'"Marvel/Marvel 20K"'},
            {'base': '"Merlin"', 'wips': '"Merlin/Merlin WIPs"', '3k': '"Merlin"', '20k':'"Merlin"'},
            {'base': '"Miraculous Ladybug"', 'wips': '"Miraculous Ladybug/Miraculous WIPs"', '3k': '"Miraculous Ladybug/Miraculous 3K"', '20k':'"Miraculous Ladybug/Miraculous 20K"'},
            {'base': '"Others"', 'wips': '"Others"', '3k': '"Others/Others 3K"', '20k':'"Misc 20K"'},
            {'base': '"Percy Jackson"', 'wips': '"Percy Jackson/PJO WIPs"', '3k': '"Percy Jackson"', '20k':'"Percy Jackson"'},
            {'base': '"Star Wars"', 'wips': '"Star Wars/Star Wars WIPs"', '3k': '"Star Wars/Star Wars 3K"', '20k':'"Star Wars/Star Wars 20K"'},
            {'base': '"The Murderbot Diaries"', 'wips': '"The Murderbot Diaries"', '3k': '"The Murderbot Diaries/The Murderbot Diaries 3K"', '20k':'"The Murderbot Diaries/The Murderbot Diaries 20K"'},
            {'base': '"The Untamed"', 'wips': '"The Untamed/Untamed WIPs"', '3k': '"The Untamed/The Untamed 3K"', '20k':'"The Untamed/The Untamed 20K"'}
            ]


def sortEmail(imap, inbox, folders, numMessages):
    status, messages = imap.select(mailbox=(inbox))
    messages = int(messages[0])

    if messages < numMessages:
        N = messages
    else:
        N = numMessages

    with alive_bar(N, title=(inbox)) as bar:
        for i in range(messages, messages-N, -1):
            complete = False
            len20k = False
            len3k = False
            len1k = False
            first = False

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
                                        # chapters = (body.split("Chapters: ")[1].split("\nFandom:")[0]).strip(" ").strip("\r").split("/")
                                        chapters = regex.findall(r"\bChapters:\s+\K\S+",body)

                                        words = re.findall(r"\((\d*?) words\)", body)
                                        # print(words)
                                        for i in range(len(chapters)):
                                            fic_chapters = chapters[i].strip(" ").strip("\r").split("/")
                                            if fic_chapters[0] == fic_chapters[1]:
                                                # print("Complete")
                                                complete = True
                                            if fic_chapters[0] == '1':
                                                first = True
                                        for i in range(len(words)):
                                            if words[i] == '':
                                                words[i] = '0'
                                            if int(words[i]) > 12000:
                                                len20k = True
                                            if int(words[i]) > 1500:
                                                len3k = True
                                            if int(words[i]) < 1000:
                                                len1k = True

                                        if len20k and complete:
                                            #longfic
                                            imap.uid('MOVE', uid ,folders['20k'])
                                            if debug:
                                                print(f"words {words} chapters {chapters} complete {complete} - moved to {folders['20k']}")

                                        elif len3k and complete:
                                            #medium fic
                                            imap.uid('MOVE', uid ,folders['3k'])
                                            if debug:
                                                print(f"words {words} chapters {chapters} complete {complete} - moved to {folders['3k']}")
                                        elif (complete or first) and not len1k:
                                            #short fic
                                            imap.uid('MOVE', uid ,folders['base'])

                                            if debug:
                                                print(f"words {words} chapters {chapters} complete {complete} - moved to {folders['base']}")
                                        elif not complete or len1k:
                                            imap.uid('MOVE', uid ,folders['wips'])
                                            if debug:
                                                print(f"words {words} chapters {chapters} complete {complete} - moved to {folders['wips']}")
                                        else:
                                            if debug:
                                                print(f"ERROR {len20k} {len3k} {len1k} {complete}")
                                            pass
                                        bar.text = subject

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

    for k in range(len(inboxes)):
        inbox = inboxes[k]['base']
        sortEmail(imap, inbox, inboxes[k], numMessages)
        inbox = inboxes[k]['wips']
        sortEmail(imap, inbox, inboxes[k], numMessages)
        inbox = inboxes[k]['3k']
        sortEmail(imap, inbox, inboxes[k], numMessages)

    # close the connection an   d logout
    imap.close()
    imap.logout()


# if __name__ == "__main__":
#     from keys import username, password
#     sortCompletedFics(username, password)
    
# sortCompletedFics(username, password)

sortCompletedFics(sys.argv[1], sys.argv[2])
