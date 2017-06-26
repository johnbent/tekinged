#! /usr/bin/env python

import sys
from sshtunnel import SSHTunnelForwarder
import MySQLdb
import MySQLdb.cursors
import pymysql
from _mysql_exceptions import IntegrityError

def pal2id(c,pal,verbose=False):
  def show_word(idx,row):
    print "\t%d: %s %s [%s] [id %d, root %d]" % (idx,row['pos'],row['eng'],row['pdef'],row['id'],row['stem'])

  c.execute("select id,pos,eng,stem,pdef from all_words3 where pal like '%s'" % pal)
  rows = c.fetchall()
  print "%s has %d matches" % (pal, len(rows))
  if (len(rows)>1):
    for idx, row in enumerate(rows):
      show_word(idx,row)
    answer = raw_input("\tWhich word to link?")
    row = rows[int(answer)]
    print "Using %s" % row['eng']
    return row['id']
  elif (len(rows)==0):
    return None
  else:
    if verbose:
      show_word(0,rows[0])
    return rows[0]['id']

def connect2():
  server = SSHTunnelForwarder(
          ('tekinged.com', 22),
          #ssh_private_key="/Users/bentj/.ssh/id_rsa",
          ssh_password="cherredochedelmeas",
          ssh_username="johnbent",
          remote_bind_address=('127.0.0.1', 3308))
  server.start()
  print "Have connection to %d" % server.local_bind_port
  con = MySQLdb.connect(user='johnbent',passwd='chemelekelbuuch',db='belau',host='127.0.0.1',port=server.local_bind_port,cursorclass=MySQLdb.cursors.DictCursor)
  cur = con.cursor()
  return (con,cur)

def print_from_row(row,indent=''):
  print "%s%06d/%06d: %-15s %5s %s" % (indent, row['stem'], row['id'], row['pal'].upper(), row['pos'], row['eng'])
  if (row['pdef']):
    print "%s\t%s" % (indent,row['pdef'])

def print_from_id(c,wid,indent=''):
  q = "select * from all_words3 where id=%d order by pal" % wid
  c.execute(q)
  assert(c.rowcount()==1) 
  word = c.fetchone()
  print_from_row(c.fetchone(),indent)

def connect():
  db=MySQLdb.connect(user="johnbent",passwd="chemelekelbuuch",db="belau",host="127.0.0.1",port=3307,cursorclass=MySQLdb.cursors.DictCursor)
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
