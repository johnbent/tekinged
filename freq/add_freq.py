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


def main():
  (db,c) = belau.connect()


  for line in fileinput.input():
    (rank, pal, count, perc) = line.split()
    q = "insert into frequency (pal,perc,quantity) values (%s,%s,%s)"
    values = (pal,perc,count)
    c.execute(q,values)
    print q, values


  #c.execute(q); 
  db.commit()
  c.close()
  db.close()
  sys.exit(0)

if __name__ == "__main__": main()


