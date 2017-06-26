#! /usr/bin/env python
# -*- coding: utf-8 -*- 

from __future__ import unicode_literals
import re
import sys
import pymysql
import codecs
import MySQLdb
import copy
import itertools
import time
import os
import random

sys.path.append('/Users/bentj/Dropbox/belau/scripts')
sys.path.append('../scripts')
import belau

total_updates=0

def insert_trivia(c,q,a,opts):
  prompt = False
  query = "insert into upload_trivia (q,a,o1,o2,o3,o4,assignee,uploaded,submitted) VALUES (%s,%s,%s,%s,%s,%s,'John Bent',1,now())"
  values = (q,a) + tuple(opts)
  try:
    print "\tExecute %s %s?" % (query, ", ".join(str(i) for i in values))
    if (prompt):
      var = raw_input("\ty|n? ")
    else:
      var = 'y'
    if (var != 'n'):
      c.execute(query,values)
      rid=c.lastrowid
      return rid
    else:
      return 0
  except: 
    e = sys.exc_info()[0]
    print "insert_trivia Error: %s" % e
    return -1

def mywarn(msg):
  answer = raw_input("WARN: %s. Continue [y|n]: " % msg)
  if (answer != 'y'):
    sys.exit(0)

def file_len(fname):
  with open(fname) as f:
    for i, l in enumerate(f):
      pass
  return i + 1


def get_answer(ans,options):
  #print "Remove %s from %s" % (ans,options)
  opts = copy.deepcopy(options) 
  opts.remove(ans)
  opts = random.sample(list(opts),4)
  return (ans,opts)

def main():
  (db,c) = belau.connect()

  inputfile='trivia.txt'
  line_count = file_len(inputfile)
  print "%s has %d lines" % (inputfile,line_count)

  lines = [line.strip() for line in open(inputfile)]

  delimiter = lines[0]
  templates = lines[1:3]
  trivia    = lines[3:]

  xs = set() 
  ys = set()

  # build up the set of items
  for item in trivia:
    (x,y) = item.split(delimiter)
    xs.add(x.strip())
    ys.add(y.strip())

  # now make a question for each
  for i,item in enumerate(trivia):
    (x,y) = item.split(delimiter)
    x = x.strip() # ugh, strip again
    y = y.strip()
    i = 0 # force to use the first template
    if (i%2==0):
      (ans,opts) = get_answer(y,ys)
      template = templates[0]
    else:
      (ans,opts) = get_answer(x,xs)
      template = templates[1]
    q = template.replace('XXX',x).replace('YYY',y)
    #template = random.choice(templates)
    print "%d T: %s -> %s [%s])" % (i, q, ans, opts)  
    insert_trivia(c,q,ans,opts)

  # commit and close
  db.commit()
  c.close()
  db.close()

if __name__ == "__main__": main()

