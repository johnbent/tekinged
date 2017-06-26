#! /usr/bin/env python

import sys
import MySQLdb
import MySQLdb.cursors
import pymysql


def connect():
  db=MySQLdb.connect(user="johnbent",passwd="chemelekelbuuch",db="belau",host="mysql.tekinged.com",cursorclass=MySQLdb.cursors.DictCursor)
  c=db.cursor()
  return (db,c)

def insert(c,db,pal,pdef=None,edef=None,prompt=True):
  query = "insert into all_words3 (pal,pdef) values (%s,%s)"
  values = (pal,pdef)
  try:
    print "Execute %s %s?" % (query, values)
    if (prompt):
      var = raw_input("y|n? ")
    else:
      var = 'y'
    if (var != 'n'):
      c.execute(query,values)
      rid=c.lastrowid
      query = "update all_words3 set stem=id where id=%s"
      c.execute(query,(rid,))
      db.commit()
      return rid
    else:
      return 0
  except: 
    e = sys.exc_info()[0]
    print "Error: %s" % e
    return -1

def print_rows(rows,word,wordtwo):
  for row in rows:
    print "%s/%s is already defined as %s" % (word,wordtwo,row[2])

def search(c,word):
  c.execute("""select id,eng,pdef,stem,id,tags,pos from all_words3 where pal like '%s'""" % (word))
  rows = c.fetchall()
  return rows
