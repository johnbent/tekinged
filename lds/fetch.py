#! /usr/bin/env python

import urllib2
from bs4 import BeautifulSoup as bs
import argparse
import sys

sys.path.append('/Users/bentj/Dropbox/belau/scripts')
sys.path.append('../scripts')
import belau

def parse_args():
  parser = argparse.ArgumentParser()
  parser.add_argument('url', type=str, help="URL to fetch")
  parser.add_argument("-v", help="Verbose",action="store_true")
  return parser.parse_args()


def main():
  args = parse_args()
  (db,c)=belau.connect()

  opener = urllib2.build_opener()
  opener.addheaders = [('User-agent', 'Mozilla/5.0')]
  response = opener.open(args.url)
  page = response.read()
  soup = bs(page)
  table = 'religious_online'
  lang = 'eng'

  ps = soup.findAll('p', {'class': ''})
  for idx,p in enumerate(ps):
    if 'lokiu a Intellectual Reserve' in p.text:
      break
    elif 'Mlara President' in p.text:
      next
    elif 'Mla er a President' in p.text:
      next
    else:
      print "%2d [%4d] %s ##########################" % (idx,len(p.text),args.url)
      if lang=='pau':
        query = "insert into %s (palauan,url,paragraph) values (%s,%s,%s)" 
      elif lang=='eng':
        query = "update " + table + " set english=%s where url like %s and paragraph = %s" 
        args.url = args.url.replace('lang=eng','lang=pau')
      else:
        print "WTF?"
      values = (p.text,args.url,idx)
      print query, values
      c.execute(query,values)

  db.commit()
  c.close()
  db.close()

  #print soup


if __name__ == "__main__": main()
