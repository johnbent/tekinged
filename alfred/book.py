#! /usr/bin/env python

import sys
import pymysql
import itertools

sys.path.append('/Users/bentj/Dropbox/belau/scripts')
sys.path.append('../scripts')
import belau


def add_book(c,t,g):

  update = "insert into books (title,category,grade) values (%s,'childrens',%s)" 
  values = (t,g)
  try:
    #print update
    c.execute(update,values)
    if (c.rowcount):
      print update
  except: 
    print "Insert error: Duplicate? %s [%s]" % (update, values)

def main():
  (db,c) = belau.connect()

  for line in open('books.txt'):
    line = line.rstrip('\r\n');
    words = line.split()
    (title,grade) = line.split(':')
    add_book(c,title,grade)

  # commit and close
  db.commit()
  c.close()
  db.close()
    
if __name__ == "__main__": main()


