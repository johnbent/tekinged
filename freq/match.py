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
  q = "select a.pal as x,b.pal as y from frequency a, frequency b where isnull(a.stem) && a.pal like concat('l', b.pal)";
  q = "select a.pal as p, a.id as i from frequency a where (isnull(a.stem) or a.stem=0) order by a.pal"; 
  c.execute(q)
  nulls = c.fetchall()
  print "%d nulls to match" % len(nulls)
  for n in nulls:
    print "%s does not yet have a stem." % (n['p'])
    q = "select * from all_words3 where pal like '%s'" % (n['p'])
    c.execute(q)
    matches = c.fetchall()
    if len(matches) == 0:
      q = "update frequency set stem=0 where pal like '%s'" % (n['p'])
      print "\t%s has no matches, setting to 0" % n['p']
      c.execute(q)
    elif len(matches) ==1:
      q = "update frequency set stem=%d where id like '%d'" % (matches[0]['id'],n['i'])
      print q
      c.execute(q)
    else:
      for idx, row in enumerate(matches):
        print "%d: %s %s [%d/%d]\n\tENG: %s\n\tPAL: %s" % (idx, row['pal'], row['pos'], row['id'], row['stem'], row['eng'], row['pdef'])
      print "\t\tWhich row to use? [n=none,q=quit,x [y]=rows"
      ans = raw_input()
      if ans == 'n':
        q = "update frequency set stem=0 where id = '%d'" % (n['i'])
        c.execute(q)
      elif ans == 'q':
        return
      else:
        ids = ans.split()
        # first of all, add the stem for the first number they entered
        q = "update frequency set stem=%d where id = '%d'" % (matches[int(ids[0])]['id'], n['i'])
        print q
        c.execute(q)
        for i in range(1,len(ids)):
          q = "insert into frequency( pal, perc, quantity ) select pal, perc, quantity from frequency where id=%d" % (n['i'])
          print q
          c.execute(q)
          rid=c.lastrowid
          q = "update frequency set stem=%d where id=%d" % (matches[i]['id'],rid)
          c.execute(q)
          print q
             


if __name__ == "__main__": main()


