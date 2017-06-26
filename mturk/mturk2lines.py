#! /bin/env python

import csv
import pymysql
import argparse
import sys
import glob
import re

sys.path.append('/Users/bentj/Dropbox/belau/scripts')
import belau

def nonblank_lines(f):
  for l in f:
    line = l.rstrip()
    if line:
      yield line

parser = argparse.ArgumentParser(description='Add phrases to the belau db')
parser.add_argument('-s', action="store", dest="s", type=int)
args = parser.parse_args()

# get a db connection
(db,c) = belau.connect()

p = re.compile("http://tekinged.com/png-halves/dict-(\d+)-(\S+).png")

inserts=0
select="select id,Input_image_url,Answer_column from mturk"
c.execute(select)
for row in c.fetchall():
  mid=row[0]
  url=row[1]
  print "%d %s" % (mid,url)
  match=p.match(url)
  pageno=int(match.group(1))
  col=match.group(2)
  for index,line in enumerate(nonblank_lines(row[2].splitlines())):
    line = line.replace(' +','')
    print "\t%d.%s.%d : %s" % (pageno,col,index,line)
    insert="insert ignore into mturk_lines (mid,url,page,col,lineno,text) values (%s,%s,%s,%s,%s,%s)"
    print insert
    c.execute(insert, (mid,url,pageno,col,index,line,))
    inserts += c.rowcount

print "%d rows inserts" % inserts
db.commit()
db.close()
