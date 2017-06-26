#! /bin/env python
# -*- coding: utf-8 -*- 

from __future__ import unicode_literals
import sys
import re
import pymysql
import codecs
import os

inputfile = 'examples.txt'

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
    parts = line.split('--')
    query = "insert into examples (palauan,english) values (%s,%s)"
    run_query(query,line.split('--'))
db.commit()
db.close()

os.unlink(inputfile)

