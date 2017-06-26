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
  do_work(c)
  db.commit()
  c.close()
  db.close()
  sys.exit(0)

def do_work(c):
  q = "select * from frequency where isnull(synonyms)";
  c.execute("select * from frequency");
  for f in c.fetchall():
    q = "select grouping from synonyms where word=%d" % f['stem']
    q = "select a.pal as pal,group_concat(a.pal) as syns from synonyms s, all_words3 a, synonyms ss where ss.word=%d and s.grouping = ss.grouping and s.word=a.id;" % f['stem']
    c.execute(q)
    syns = c.fetchone()
    if syns['syns'] is not None:
      s = set(syns['syns'].split(','))
      s.remove(f['pal'])
      nice = ','.join(s)
      print "%s has syns %s" % (f['pal'],nice)
      q = "update frequency set synonyms='%s' where id=%s" % (nice,f['id'])
      print q
      c.execute(q)

if __name__ == "__main__": main()


