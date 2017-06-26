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

def insert_image(c,p):
  prompt = False
  p = p + 1
  query = "update dekaingeseu_charlotte set image=1 where page=%d" % p
  try:
    if (prompt):
      var = raw_input("\ty|n? ")
    else:
      var = 'y'
    if (var != 'n'):
      c.execute(query)
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

  inputfile='charlotte.txt'
  line_count = file_len(inputfile)
  print "%s has %d lines" % (inputfile,line_count)

  lines = [line.strip() for line in open(inputfile)]

  for line in lines:
    p = line.strip()
    print "%d -> %d" % (int(p),int(p)+1)
    insert_image(c,int(p))

  # commit and close
  db.commit()
  c.close()
  db.close()

if __name__ == "__main__": main()

