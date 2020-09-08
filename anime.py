import sys
import re
import urllib.request 


mflag = False # add others later
rflag = False
iflag = False
sname = ""

for i in range(1,len(sys.argv)):
    if sys.argv[i][0] == "-":
        for c in sys.argv[i]:
            if c == "m": mflag = True
            if c == "r": rflag = True
            if c == 'i': iflag = True
    else:
        sname += " " + sys.argv[i]  # nervous about this, but seems to work
                                    # combines remaining args to make multi word names

sname = sname.strip() # remove leading space
sname = sname.replace(" ", "_")

sh = urllib.request.urlopen("http://myanimelist.net/anime.php?q="+sname+"&cat=anime").read()
sh = sh.decode("utf-8") # get the search page

pat = re.compile('myanimelist.net/anime/\d+/[a-zA-Z0-9_-]+') # look for anime matches
m = re.search(pat, sh)

if (m is None):
    print("no matches were found (this is probably our fault)") # catch searches w/ no match, probably won't happen
    exit()

link = sh[m.start(): m.end()] # snag url of first hit
  
page = urllib.request.urlopen("http://" + link).read()
page = page.decode("utf-8") # get html of page of anime we are about
page = re.sub('&amp;', '&', page); # clean &s in html

if iflag: # all sidebar info 
    infopat = re.compile('<h2>Information.+?Statistics', re.DOTALL)
    infom = re.search(infopat, page)
    interesting = re.sub('(<.+?>)', '', page[infom.start():infom.end()-10]) # remove tags, leave contents
    interesting = re.sub(' +', ' ', interesting) # colapse spaces and tabs to 1 space
    interesting = re.sub('^\w+$', '', interesting) # remove lines w/o spaces (hacky and should be cleaned up)
    interesting = re.sub(':\n', ':', interesting) # make Title: \n name into one line. 
    interesting = re.sub(r'([A-Z][a-z0-9]+)\1', r'\1', interesting) # remove duplicated text 
    # (for some reason the genres are listed twice, so this changes FantasyFantasy to just Fantasy. Relies of capitalization of genres) 
    for l in interesting.split('\n'):
        if (len(l) > 2): # removes random lines w/ " \n" on them. not sure why these exist
            print(l)
    print()
    
if mflag: # description of anime (main body of mal)
    titlepat = re.compile('title-name.+</h1>') 
    descpat = re.compile('itemprop.{2}description.+?</p>', re.DOTALL)
    titlem = re.search(titlepat, page)    
    descm = re.search(descpat, page)
    print(page[titlem.start()+12 : titlem.end()-5]) # name of series
    print(page[descm.start()+23 : descm.end()-4].replace("<br />", "")) # description
    print()


# thoughts: maybe we should add a title at the top of the info section, it doesn't have one. 
# the user needs to be sure that they actually got the series they were looking for
# which is not a guarantee given how wack mal search is

# need to add the recommendation section

# instead of downloading, maybe just print out where you could find it? idk man

