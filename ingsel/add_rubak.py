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
    line = line.rstrip()
    if len(line) > 0:
      print line
      q = "insert into translate_rubak (english) values (%s)"
      values = (line,)
      c.execute(q,values)

  db.commit()
  c.close()
  db.close()
  sys.exit(0)

if __name__ == "__main__": main()


