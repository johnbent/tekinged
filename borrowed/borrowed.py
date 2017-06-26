#! /bin/env python
# -*- coding: utf-8 -*- 

from __future__ import unicode_literals
import sys
import re
import pymysql
import codecs

def cannot(p,e,o,y):
  print "CANNOT DO %s -> %s (%s): %s" % (p,e,o,y)

def run_query(query):
  #print query
  try:
    c.execute(query)
    db.commit()
  except: 
    e = sys.exc_info()[0]
    print "Error: %s" % e

db=pymysql.connect(user="johnbent",passwd="0730Remliik",db="belau",host="mysql.tekinged.com")
c=db.cursor()
p = re.compile('(^\S+)\s+‘(.*?)’\s+\((.+)\)')
for line in codecs.open('borrowed.txt'):
    line = line.decode('utf-8').strip()
    #line = line.rstrip('\r\n');
    try:
      m = p.match(line)
      pal = m.group(1)
    except AttributeError:
      continue # probably a blank line
    eng = m.group(2)
    org = m.group(3)
    if '/' in pal or '(' in pal:
      cannot(pal,eng,org,"has punctuation")
      continue
    try:
      pass
      #print "%s -> %s -> %s" % (pal,eng,org)
    except UnicodeEncodeError:
      cannot(pal,eng,org,"has UnicodeError")
      sys.exit(0)
    query = "select stem from all_words3 where pal like '%s'" % pal
    run_query(query)
    if (c.rowcount == 0):
      query = "insert into all_words3 (pal,eng,origin) values ('%s','%s','%s')" % (pal,eng,org)
    elif (c.rowcount == 1):
      query = "update all_words3 set origin='%s' where pal like '%s'" % (org,pal)
    else:
      cannot(pal,eng,org,"has too many matches in db")
      continue
    #print query
    #run_query(query)
    #print "%d rows for %s" % (c.rowcount,pal)
db.close()

