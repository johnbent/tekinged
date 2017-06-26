#! /bin/env python
# -*- coding: utf-8 -*- 

from __future__ import unicode_literals
import sys
import re
import pymysql
import codecs
import os
import argparse

parser = argparse.ArgumentParser(description='Add phrases to the belau db')
parser.add_argument('-s', action="store", dest="s", type=int)
args = parser.parse_args()

inputfile = 'phrase.txt'

def run_query(query,values):
  print "%s -> %s" % (query,values)
  try:
    c.execute(query,values)
    db.commit()
    return c.lastrowid
  except: 
    e = sys.exc_info()[0]
    print "Error: %s" % e
    return -1

db=pymysql.connect(user="johnbent",passwd="chemelekelbuuch",db="belau",host="mysql.tekinged.com")
c=db.cursor()
for line in codecs.open(inputfile):
    line = line.decode('utf-8').strip()
    line = line.replace('’', "'")
    values = line.split('--')
    if (args.s):
      query = "insert into all_words3 (pal,eng,stem,pos) values (%s,%s,%s,'expression')"
      values.append(args.s)
    else:
      query = "insert into all_words3 (pal,eng,pos) values (%s,%s,'expression')"
    run_query(query,values)
db.commit()
db.close()

os.unlink(inputfile)

