__author__ = 'wdolowicz'


import sys
from iphone import edit_iphone
from iphone import send_iphone
from ipad import edit_ipad
from ipad import send_ipad
from ands import edit_ands
from ands import send_ands
from andt import edit_andt
from andt import send_andt

platform = sys.argv[1]
version = sys.argv[2]
textfile = sys.argv[3]
me = "mail@yourmail.com"
password = "password"
addresslist = sys.argv[4]
recipients_text = open(addresslist, "r")
list1 = recipients_text.readlines()
you = ", ".join(list1).replace('\n', '')

if platform == 'iphone':
    edit_iphone(version, textfile)
    send_iphone(version, me, password, you)
elif platform == 'ipad':
    edit_ipad(version, textfile)
    send_ipad(version, me, password, you)
elif platform == 'ands':
    edit_ands(version, textfile)
    send_ands(version, me, password, you)
elif platform == 'andt':
    edit_andt(version, textfile)
    send_andt(version, me, password, you)
else:
    print("Error: incorrect platform given")

list = list1
print('New version notification has been sent to following adresses: ' + '\n' + ''.join(list))
