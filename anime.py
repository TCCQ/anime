import sys
import re
import urllib.request 


mflag = False # add others later
rflag = False
sname = ""

for i in range(1,len(sys.argv)):
    if sys.argv[i][0] == "-":
        for c in sys.argv[i]:
            if c == "m": mflag = True
            if c == "r": rflag = True
    else:
        sname += " " + sys.argv[i] # assumes that name is treated as seperate args for each word
    # not sure if anime -r "one plus words" would break it
    # probably shell would kill the quotes and pass it all as one but idk
    # I guess it would still be fine

sname = sname.strip() # remove leading space
sname = sname.replace(" ", "_")


sh = urllib.request.urlopen("http://myanimelist.net/anime.php?q="+sname+"&cat=anime").read()

sh = sh.decode("utf-8")

# print(sh)

pat = re.compile('myanimelist.net/anime/\d+/[a-zA-Z0-9_-]+')



m = re.search(pat, sh)
if (m is None):
    print("no matches were found (this is probably our fault)")
    exit()

link = sh[m.start(): m.end()]
  
page = urllib.request.urlopen("http://" + link).read()
page = page.decode("utf-8")

titlepat = re.compile('title-name.+</h1>')

descpat = re.compile('itemprop.{2}description.+?</p>', re.DOTALL)

descm = re.search(descpat, page)
titlem = re.search(titlepat, page)

if (descm is None):
    print("no matches were found the second time")
    exit()

if mflag:
    print(page[titlem.start()+12 : titlem.end()-5])
    print(page[descm.start()+23 : descm.end()-4].replace("<br />", "")) #description




