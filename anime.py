import sys
import urllib as web
from googlesearch import lucky
# https://python-googlesearch.readthedocs.io/en/latest/_modules/googlesearch.html

mflag = False # add others later
rflag = False
sname = ''

for i in range(1,len(sys.argv)):
    if sys.argv[i][0] == '-':
        for c in sys.argv[i]:
            if c == 'm': mflag = True
            if c == 'r': rflag = True
    sname += ' ' + sys.argv[i] # assumes that name is treated as seperate args for each word
    # not sure if anime -r "one plus words" would break it
    # probably shell would kill the quotes and pass it all as one but idk
    # I guess it would still be fine


sname = sname.strip() # remove leading space

query = "site:myanimelist.net " + sname


  
print(lucky(query))






