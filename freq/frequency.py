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

def combine(args,c,verbose=False):
  root = None
  total_p = 0
  total_q = 0

  for arg in args: 
    q = "select * from frequency where pal like '%s'" % arg
    c.execute(q)
    rows = c.fetchall()
    total_p += rows[0]['perc']
    total_q += rows[0]['quantity']
    if root is None:
      root = rows[0]['id']
    else:
      q = "delete from frequency where id = '%d'" % rows[0]['id']
      if verbose:
        print q
      c.execute(q)
    print rows[0]
  print "%s shoudl be %.3f : %d" % (root, total_p, total_q)
  q = "update frequency set perc=%f, quantity=%d where id=%d" % (total_p, total_q, root)
  if verbose:
    print q
  c.execute(q)

