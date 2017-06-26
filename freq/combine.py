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
  f.combine(sys.argv[1:],c,True)

  db.commit()
  c.close()
  db.close()
  sys.exit(0)

if __name__ == "__main__": main()


