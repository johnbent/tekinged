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

def insert_sentence(c,p,e):
  prompt = False
  query = "insert into upload_sentence (palauan,eng,assignee,uploaded,submitted) VALUES (%s,%s,'Jelga Emiwo',1,now())"
  values = (p,e) 
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

def main():
  (db,c) = belau.connect()

  inputfile='sentences.txt'
  line_count = file_len(inputfile)
  print "%s has %d lines" % (inputfile,line_count)

  lines = [line.strip() for line in open(inputfile)]

  delimiter = '/' 

  for line in lines:
    (p,e) = line.split(delimiter)
    p = p.strip()
    e = e.strip()
    print "%s -> %s" % (p,e)
    insert_sentence(c,p,e)

  # commit and close
  db.commit()
  c.close()
  db.close()

if __name__ == "__main__": main()

