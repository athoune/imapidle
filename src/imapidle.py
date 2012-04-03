import imaplib


def idle(connection):
    tag = connection._new_tag()
    connection.send("%s IDLE\r\n" % tag)
    response = connection.readline()
    connection.loop = True
    if response == '+ idling\r\n':
        while connection.loop:
            yield connection.readline()
    else:
        raise Exception("IDLE not handled? : %s" % response)

imaplib.IMAP4.idle = idle

if __name__ == '__main__':
    import os
    user = os.environ['EMAIL']
    password = os.environ['PASSWORD']
    print os.environ['SERVER']
    m = imaplib.IMAP4_SSL(os.environ['SERVER'])
    m.login(user, password)
    m.select()
    for msg in m.idle():
        print msg
