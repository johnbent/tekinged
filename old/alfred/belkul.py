#! /bin/env python

import sys
import pymysql
import os

wordfile='belkul.txt'

def run_query(query):
  print query
  try:
    c.execute(query)
    db.commit()
  except: 
    e = sys.exc_info()[0]
    print "Error: %s" % e

db=pymysql.connect(user="johnbent",passwd="0730Remliik",db="belau",host="mysql.tekinged.com")
c=db.cursor()
for line in open(wordfile):
    line = line.rstrip('\r\n');
    words = line.split()
    pal = words.pop(0)
    pos = words.pop(0)
    eng = ' '.join(words)
    query = "insert into all_words3 (pal,pos,eng) values ('%s','%s','%s')" % (pal,pos,eng)
    run_query(query)
db.close()

os.unlink(wordfile)
