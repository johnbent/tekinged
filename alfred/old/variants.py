#! /bin/env python

import sys
import pymysql

db=pymysql.connect(user="johnbent",passwd="0730Remliik",db="belau",host="mysql.tekinged.com")
c=db.cursor()
for line in open('variants.txt'):
    line = line.rstrip('\r\n');
    (a,b) = line.split()
    query = "insert into variants (a,b) values ('%s','%s')" % (a,b)
    try:
      #print update
      c.execute(query)
      if (c.rowcount):
        print query
      db.commit()
    except: 
      e = sys.exc_info()[0]
      print "Error: %s" % e
db.close()

