#! /usr/bin/env python

import sys
import pymysql
import string
import re
import os
import fileinput

sys.path.append('/Users/bentj/Dropbox/belau/scripts')
sys.path.append('../scripts')
import belau

import frequency as f


def main():
  (db,c) = belau.connect()

  # use split if you are splitting something like 'ng' off the front of the word and want to update 'ng' also
  split = False

  q = "select a.pal as x,b.pal as y from frequency a, frequency b where isnull(a.stem) && a.pal like concat('l', b.pal)";
  q = "select a.pal as x,b.pal as y from frequency a, frequency b where isnull(a.stem) && a.pal like concat('m', b.pal)";
  q = "select a.pal as x,b.pal as y, b.perc as p, b.quantity as q from frequency a, frequency b where isnull(a.stem) && a.pal like concat('ng', b.pal)";
  q = "select a.pal as x,b.pal as y, a.perc as p, a.quantity as q from frequency a, frequency b where a.pal like concat('ng',b.pal)";
  q = "select a.pal as x,b.pal as y, a.perc as p, a.quantity as q from frequency a, frequency b where (a.stem=0 or b.stem=0) and a.pal like concat('le',b.pal)";
  q = "select a.pal as x,b.pal as y, a.perc as p, a.quantity as q from frequency a, frequency b where (a.stem=0 or b.stem=0) and a.pal like concat(b.pal,'ng')";
  q = "select a.pal as x,b.pal as y, a.perc as p, a.quantity as q from frequency a, frequency b where (a.stem=0 or b.stem=0) and a.pal like concat('l',b.pal)";
  q = "select a.pal as x,b.pal as y, a.perc as p, a.quantity as q from frequency a, frequency b where (a.stem=0 or b.stem=0) and a.pal like concat('m',b.pal)";
  c.execute(q)
  c.execute(q)
  for row in c.fetchall():
    print "Merge %s into %s? [y|n]" % (row['x'], row['y'])
    ans = raw_input()
    if ans == 'y':
      try:
        f.combine((row['y'],row['x']),c,True)
        if split == True:
          qq = "update frequency set quantity=quantity+%d,perc=perc+%f where pal like 'le'" % (row['q'],row['p'])
          print qq
          c.execute(qq)
      except IndexError:
        print "Index Error"
    elif ans == 'q':
      break

  db.commit()
  c.close()
  db.close()
  sys.exit(0)

if __name__ == "__main__": main()


