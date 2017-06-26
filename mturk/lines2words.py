#! /bin/env python

from difflib import SequenceMatcher
import itertools
import csv
import pymysql
import argparse
import sys
import glob
import re

sys.path.append('/Users/bentj/Dropbox/belau/scripts')
import belau

def fuzz(s1,s2):
  m = SequenceMatcher(None, s1.lower(), s2.lower()) 
  return m.ratio() 

parser = argparse.ArgumentParser(description='Add phrases to the belau db')
parser.add_argument('-t', action="store", dest="threshold", type=float, default=0.95)
args = parser.parse_args()

# get a db connection
(db,c) = belau.connect()

q="select distinct(concat(page,'.',col,'.',lineno)) from mturk_lines"
c.execute(q)
perfect=0
good=0
bad=0
for row in c.fetchall():
  (page,col,line) = row[0].split('.')
  compare="select text from mturk_lines where page=%s and col=%s and lineno=%s"
  c.execute(compare,(page,col,line,))
  rows=list(c.fetchall())
  for a, b in itertools.combinations(rows, 2):
    word=a[0].split()[0]
    fz=fuzz(a[0],b[0])  
    if (fz==1):
      perfect=perfect+1
    if (fz>args.threshold):
      good=good+1
    else:
      bad=bad+1
    print "%s %s %s : %.3f" % (page,col,word,fz)
     
print "%d perfect. %d good matches. %d bad matches" % (perfect,good,bad)

