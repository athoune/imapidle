import imaplib


def idle(connection):
    tag = connection._new_tag()
    connection.send("%s IDLE\r\n" % tag)
    response = connection.readline()
    connection.loop = True
    if response == '+ idling\r\n':
        while connection.loop:
            resp = connection.readline()
            uid, message = resp[2:-2].split(' ')
            yield uid, message
    else:
        raise Exception("IDLE not handled? : %s" % response)


def done(connection):
    connection.send("DONE\r\n")
    connection.loop = False

imaplib.IMAP4.idle = idle
imaplib.IMAP4.done = done

if __name__ == '__main__':
    import os
    user = os.environ['EMAIL']
    password = os.environ['PASSWORD']
    print os.environ['SERVER']
    m = imaplib.IMAP4_SSL(os.environ['SERVER'])
    m.login(user, password)
    m.select()
    loop = True
    while loop:
        for uid, msg in m.idle():
            print uid, msg
            if msg == "EXISTS":
                m.done()
                typ, data = m.fetch(uid, '(RFC822)')
                print typ
                print data
