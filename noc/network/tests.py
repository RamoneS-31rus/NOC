from django.test import TestCase

# Create your tests here.
import re

ipv4_re = (
            r'(?:25[0-5]|2[0-4]\d|1\d?\d?|[1-9]\d?)'
            r'(?:\.(?:0|25[0-5]|2[0-4]\d|1\d?\d?|[1-9]\d?)){3}'
        )

mac_re = (
        r'(?:[0-9a-fA-F]{2})'
        r'(?:(\:|\-)(?:[0-9a-fA-F]{2})){5}'
)

serial_re = (
        r'[a-zA-Z]+'
)

value = 'F0:7D:68:A4:53:61'

if re.match(serial_re, value):
    print('TRUE')
else:
    print('FALSE')




"""

r"(?:0|25[0-5]|2[0-4]\d|1\d?\d?|[1-9]\d?)"
r"(?:\.(?:0|25[0-5]|2[0-4]\d|1\d?\d?|[1-9]\d?)){3}"

"""