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

def get_content(url,opener):
  soup = get_soup(url,opener)
  content = soup.find('meta', {"property":"og:description"})['content']
  try:
    nextpage = soup.find('a', {"class":"chapter-nav-right"})['href']
  except:
    nextpage = None
  return content,nextpage 
          

def get_soup(url,opener):
  response = opener.open(url)
  page = response.read()
  soup = bs(page, 'html.parser')
  return soup

def get_page(url):
  o = urllib2.build_opener()
  o.addheaders = [('User-agent', 'Mozilla/5.0')]
  p,npage = get_content(url,o)
  e = get_content(url.replace('PAUUBS','ENGESV'),o)[0]
  q = "insert into religious_online (palauan,english,url) values (%s,%s,%s)" 
  v = (p,e,url)
  print q, v
  if npage[0:4] != 'http':
    print "########### Fixing stupid partial link"
    npage = 'http://www.bible.is/' + npage
  return (q,v,npage)




def main():
  args = parse_args()
  (db,c)=belau.connect()

  url = args.url
  while True:
    (q,v,nextpage) = get_page(url)
    c.execute(q,v)
    db.commit()
    if nextpage is None:
      break
    url = nextpage

  db.commit()
  c.close()
  db.close()

  #print soup


if __name__ == "__main__": main()
