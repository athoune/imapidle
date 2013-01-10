# Copyright (c) 2012 Mathieu Lecarme
# This code is licensed under the MIT license (see LICENSE for details)

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
    from lamson.mail import MailRequest
    user = os.environ['EMAIL']
    password = os.environ['PASSWORD']
    print os.environ['SERVER']
    conn = imaplib.IMAP4_SSL(os.environ['SERVER'])
    conn.login(user, password)
    conn.select()
    loop = True
    while loop:
        for uid, msg in conn.idle():
            print uid, msg
            if msg == "EXISTS":
                conn.done()
                status, datas = conn.fetch(uid, '(RFC822)')
                m = MailRequest('localhost', None, None, datas[0][1])
                print m.keys()
                print m.all_parts()
                print m.is_bounce()
