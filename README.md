IMAP IDLE
=========

Handling [IDLE](http://tools.ietf.org/html/rfc2177) connection with Python,
without thread or strange things.

It's a monkey patch, all other code came from python imaplib.

Status
------

Early POC.

Example
-------

```python
from imapidle import imaplib

m = imaplib.IMAP4_SSL('imap.gmail.com')
m.login('robert', 'pa55w0rd')
m.select()
for uid, msg in m.idle():
    print msg
```

Licence
-------

MIT © Mathieu Lecarme 2012
