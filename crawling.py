# -*- coding: utf-8 -*-

import mechanize
import re
from mechanize import Browser,LinkNotFoundError
import codecs



f=codecs.open('out.txt',mode = 'w', encoding = 'utf-8')

br = mechanize.Browser()
br.open("http://rockplace.forumotion.net/f18-forum")

nextPage = 0
while nextPage == 0: #pages in forum
  url = br.geturl()
  nextElement = 0

  while nextElement >= 0:  #topics on page
    try:
      br.follow_link(url_regex=r"t[0-9]*\-topic$", nr=nextElement)
      nextElement += 1

      print unicode(br.title(), 'cp1251', 'ignore')
      print >>f, unicode(br.title(), 'cp1251', 'ignore'), br.geturl()
      #f.write (unicode(br.title(), 'cp1251', 'ignore'))
      
      br.open(url) # go back to home page
    except LinkNotFoundError:
      nextElement = -1 #last topic

  try:
    br.open(url)
    br.follow_link(url_regex=r"p[0-9]*\-forum$", nr=0)
    print "Next Page"
  except LinkNotFoundError:
    nextPage=-1

f.close()