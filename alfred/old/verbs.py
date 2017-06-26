#! /bin/env python
# -*- coding: utf-8 -*- 

from __future__ import unicode_literals
import sys
import re
import pymysql
import codecs
import os

verbfile = 'verbs.txt'

def cannot(p,e,o,y):
  print "CANNOT DO %s -> %s (%s): %s" % (p,e,o,y)

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
get_stem = re.compile('(^\S+)\s+(\S+)\s+(.*)')
p = re.compile('(^\S+)\s+‘(.*?)’\s+\((.+)\)')
for line in codecs.open(verbfile):
    line = line.decode('utf-8').strip()
    line = line.replace('’', "'")
    #line = line.encode('latin-1','ignore')
    parts = line.split('--')
    #print line
    #print parts
    stem_match = get_stem.match(parts[0])
    perfectives = parts[1].split()

    # insert the stem and set its stem to itself
    query = "insert into all_words3 (pal,pos,eng) values (%s,%s,%s)"
    stem = run_query(query,(stem_match.group(1),stem_match.group(2),stem_match.group(3),))
    query = "update all_words3 set stem=id where id=%s"
    run_query(query,(stem,))

    # insert the perfectives
    if ('terir' in perfectives[1]):
      posarray=('v.pf.3s','v.pf.3p.human','v.pf.3s.past', 'v.pf.3p.human.past')
    else:
      posarray=('v.pf.3s','v.pf.3p.inan','v.pf.3s.past', 'v.pf.3p.inan.past')
    for idx, pos in enumerate(posarray):
      query = "insert into all_words3 (pal,pos,stem) values (%s,%s,%s)"
      run_query(query, (perfectives[idx],pos,stem))

    # now everything else
    for part in parts[2:]:
      pieces = part.split()
      pal = pieces[0]
      pos = pieces[1]
      eng = ' '.join(pieces[2:])
      query = "insert into all_words3 (pal,pos,stem,eng) values (%s,%s,%s,%s)"
      run_query(query, (pal,pos,stem,eng,))
db.commit()
db.close()

os.unlink(verbfile)

