# -*- coding: utf-8 -*-

import mechanize
import re
from mechanize import Browser,LinkNotFoundError
import codecs
from operator import itemgetter
import getopt
import sys

maxPages = 99 # maximum pages to crawl in
perPage = 33 # topics per page - used to determine next page url
silent = False # if silent is true - don't print.
out = "out" # name of output file (out by default)


# reads link and output file name for forum from input
optlist, args = getopt.getopt(sys.argv[1:], 'su:o:', ["url=", "output="])

for optpair in optlist:
    opt, arg = optpair
    if opt in ("-u", "--url"):
      url = arg
    elif opt in ("-o", "--output"):
      out = arg
    elif opt == "-s":
      silent = True

# open output file in utf-8 encoding
f=codecs.open('output/'+out+'.txt' ,mode = 'w', encoding = 'utf-8')
# initializing list of data
data = [0]

# make instance of browser 
br = mechanize.Browser()
br.open(url)

# current page
page = 1
while page>0:
  url = br.geturl()
  nextElement = 0
  
  # topics on page
  while nextElement >= 0:  
    try:
      br.follow_link(url_regex=r"t[0-9]*\-topic$", nr=nextElement)
      nextElement += 1

      # extract title and url (add in data)
      if not silent:
        print 'Crawling: '+ unicode(br.title(), 'cp1251', 'ignore')
      data.append( ( unicode(br.title(), 'cp1251', 'ignore'), br.geturl() ) )
      
      
      # go back to home page
      br.open(url) 

    #last topic
    except LinkNotFoundError:
      nextElement = -1 

  try:
    br.open(url)
    regEx = r"p"+ str(perPage*page) +"\-forum$"
    if page != maxPages:
      br.follow_link(url_regex=regEx, nr=0)
      if not silent:
        print "Next Page"
      page += 1

  #last page
  except LinkNotFoundError:
    page=-1

# remove the element for init; turn to set to eliminate duplicates; sort
data.remove(0)
data = set(data)
data = sorted(data, key = itemgetter(0))

# printing in output file in form for publishing in the forum
for i in data:
  topic, link = i
  if not silent:
    print "Adding: "+topic + " " + link
  print >>f, '[url='+link+']'+topic+'[/url]'

f.close()

sys.exit(0)