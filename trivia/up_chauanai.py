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

  inputfile='all/which.txt'
  line_count = file_len(inputfile)
  print "%s has %d lines" % (inputfile,line_count)

  lines = [line.strip() for line in open(inputfile)]

  delimiter = ':' 

  q='Ngera ikang ng chauanai?'

  for line in lines:
    (w,o,a) = [x.strip() for x in line.split(delimiter)] 
    opts = [x.strip() for x in o.split(',')]
    try:
      del opts[4:]
    except:
      pass
    print "%s : %s : %s" % (w,opts,a)
    insert_trivia(c,q,a,opts)

  # commit and close
  db.commit()
  c.close()
  db.close()

if __name__ == "__main__": main()

