import imaplib
import email
from email.header import decode_header
from collections import Counter
import progressbar
import csv
import datetime
from keys import username, password

def countFandomsInInbox(username, password):

    ## https://thepythoncode.com/article/reading-emails-in-python

    imap_server = "imap.mail.yahoo.com"
    # create an IMAP4 class with SSL 
    imap = imaplib.IMAP4_SSL(imap_server)
    # authenticate
    imap.login(username, password)

    status, messages = imap.select("INBOX")

    # total number of emails
    messages = int(messages[0])
    # number of top emails to fetch
    N = messages
    # N = 50

    # print(imap.list())


    widgets = [' [',
            progressbar.Timer(format= 'elapsed time: %(elapsed)s'),
            '] ',
            progressbar.Bar('*'),' (',
            progressbar.ETA(), ') ',
            ]
    
    # bar = progressbar.ProgressBar(max_value=N, 
    #                               widgets=widgets).start()
    bar = progressbar.ProgressBar(maxval=N).start()

    fandoms = []

    count = 0
    for i in range(messages, messages-N, -1):


        # fetch the email message by ID
        res, msg = imap.fetch(str(i), "BODY.PEEK[]")
        for response in msg:
            if isinstance(response, tuple):
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
                                    body = body.split("-----------------------------------------")[0]
                                    body = body.split("=========================================")[1]
                                    fandom = body.split("Fandom: ")[1]
                                    fandom = fandom.split("Rating:")[0]
                                    fandom = fandom.replace("\r","").strip("\n")
                                    fandom = fandom.replace(", and ", ",").split(",")
                                    # print(fandom)
                                    for h in range(len(fandom)):
                                    #print(fandom)
                                        fandoms.append(fandom[h].lstrip(" and "))
                                    count += 1
                                    bar.update(count)
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

    # close the connection and logout
    imap.close()
    imap.logout()

    print("\n")
    # Counter(fandoms).keys() # equals to list(set(words))
    # Counter(fandoms).values() # counts the elements' frequency
    # count_dict = dict(Counter(fandoms).items())
    od = dict(sorted(Counter(fandoms).items(), key=lambda item: item[1], reverse=True))
    for k, v in od.items(): 
        print(k + " : " + str(v))

    date = datetime.date.today().strftime('%Y-%m-%d')
    with open(date + ' fandoms.csv', 'w', newline="", encoding='utf-8') as csvfile:
        z = csv.writer(csvfile)
        for new_k, new_v in od.items():
            z.writerow([new_k, new_v])
    # print(od)
            
if __name__ == "__main__":
    countFandomsInInbox(username, password)