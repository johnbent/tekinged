#! /usr/bin/env python
# -*- coding: utf-8 -*- 

from __future__ import unicode_literals
import sys
import pymysql
import codecs
import MySQLdb

sys.path.append('/Users/bentj/Dropbox/belau/scripts')
import belau

def insert_word(c,pword,pos,edef,stem=None,prompt=True):
  prompt=True # force prompt
  query = "insert into all_words3 (pal,pos,eng,stem) values (%s,%s,%s,%s)"
  values = (pword,pos,edef,stem)
  try:
    print "\tExecute %s %s?" % (query, ",".join(values))
    if (prompt):
      var = raw_input("\ty|n? ")
    else:
      var = 'y'
    if (var != 'n'):
      c.execute(query,values)
      rid=c.lastrowid
      if stem==None:
        query = "update all_words3 set stem=id where id=%s"
        c.execute(query,(rid,))
      return rid
    else:
      return 0
  except: 
    e = sys.exc_info()[0]
    print "Error: %s" % e
    return -1

def root_word(pieces,c):
  print "Root word %s" % pieces
  extras = []
  while (pieces[1][0] == '-'):
    extras.append(pieces[1:3])
    del pieces[1:3]
  
  pword=pieces[1]
  pos=pieces[2]
  edef=' '.join(pieces[3:])

  wid=add_word(c,pword,pos,edef)

  if len(extras)>0:
    for extra in extras:
      print "\tSliced out %s" % extra
      (flag,value) = (extra[0],extra[1])
      if (flag == '-t' or flag == '-o'):
        field = "tags" if flag == '-t' else "origin"
        query = "update all_words3 set %s=%s where id=%s" % field
        values = (value,wid)
        update_db(c,query,values)
      else:
        print "Not yet handling extra arg %s %s" % (flag,value)
        sys.exit(0)

  return wid

def add_example(c,pal,eng,wid):
  query = "insert into examples (palauan,english,source,stem) values (%s,%s,%s,%s)"
  values = (pal,eng,'Josephs',wid)
  try:
    update_db(c,query,values)
  except MySQLdb.IntegrityError:
    print "Ignoring exception on insert.  Probably duplicate."

def add_word(c,pword,pos,edef,root=None):
  # first let's make sure the pos is valid
  try:
    if (pos not in add_word.pos):
      print "\t%s is unknown pos" % pos
      sys.exit(0)
  except AttributeError:
    add_word.pos = [] 
    query="select distinct(pos) as pos from all_words3";
    c.execute(query)
    rows = c.fetchall()
    for row in rows:
      add_word.pos.append(row['pos'])
    print add_word.pos

  print "\tSearching for %s, %s, %s" % (pword,pos,edef)
  rows=belau.search(c,pword)

  # easy case.  The word not in at all.  Go ahead and add
  if (len(rows)==0):
    print "\tAdding missing word %s" % pword
    return insert_word(c,pword,pos,edef,stem=root,prompt=False)
    
  # check whether it is already entered
  for row in rows:
    if (edef == row['eng'] and pos == row['pos']):
      # easy case.  Already in with this def and pos.
      print "\t%s already in with id %d stem %d." % (pword,row['id'],row['stem'])
      return row['stem']

  # is it already in but in a different form?
  for idx, row in enumerate(rows):
    print "\t%d: Add to %s %s [%s] [id %d, root %d]" % (idx,row['pos'],row['eng'],row['pdef'],row['id'],row['stem'])
  nword = 'N' 
  skip  = 'S' 
  update = 'U'
  instead = 'I'
  print "\t%s: As a new word" % nword 
  print "\t%s: Update existing to link to this group" % update 
  print "\t%s: Do not enter right now" % skip 
  print "\t%s: Do not enter now but use this word as the root for the rest of the group." % instead
  answer = raw_input("\tEnter your choice: ")
  if (answer == nword):
    print "\tWill insert %s -> %s" % (pword, edef)
    return insert_word(c,pword,pos,edef,stem=root,prompt=False)
  elif (answer == skip):
    print "\tWill skip for now"
    return -1
  elif (answer == instead):
    if (len(rows)>1):
      answer = raw_input("\tWhich word to update")
    else:
      answer = 0
    return rows[int(answer)]['stem']
  elif (answer == update and root != None):
    if (len(rows)>1):
      answer = raw_input("\tWhich word to update")
    else:
      answer = 0
    query = "update all_words3 set stem=%s,pos=%s where id=%s"
    values = (root,pos,rows[int(answer)]['id'])
    update_db(c,query,values,prompt=False)
    return root
  elif (answer < nword):
    query = "update all_words3 set eng=%s,pos=%s where id=%s"
    values = (edef,pos,rows[int(answer)]['id'],)
    update_db(c,query,values,prompt=False)
    return rows[int(answer)]['stem']
  else:
    print "Non-sensical answer.  Exiting."
    sys.exit(0)

def update_db(c,query,values,prompt=True):
  print "\tWill update with %s %s" % (query, values)
  if prompt:
    raw_input("\tContinue")
  c.execute(query,values)


def add_perfectives(c,perf_string,root):
  print "\tAdding perfectives for root %s" % root
  perfectives = perf_string.replace(',','').split() # strip any commas
  # insert the perfectives
  if ('terir' in perfectives[1]):
    posarray=('v.pf.3s','v.pf.3p.human','v.pf.3s.past', 'v.pf.3p.human.past')
  else:
    posarray=('v.pf.3s','v.pf.3p.inan','v.pf.3s.past', 'v.pf.3p.inan.past')
  for idx, pos in enumerate(posarray):
    add_word(c,perfectives[idx],pos,None,root=root)

def add_branch(c,branch,root):
  print "\tNeed to add branch %s to %s" % (branch,root)
  pieces = branch.split()
  pword = pieces[0]
  pos = pieces[1]
  edef = ' '.join(pieces[2:])
  add_word(c,pword,pos,edef,root)

def add_link(c,a,b):
  print "Need to link %s and %s" % (a,b)

  stems = []
  linkable = True

  for word in ( a , b ):
    if word.isdigit():  # might already be the ids
      stems.append(word)
      continue
    c.execute("""select id,pos,eng,stem,pdef from all_words3 where pal like '%s'""" % word)
    rows = c.fetchall()
    if (len(rows)>1):
      print "%s has %d matches" % (word, len(rows))
      for idx, row in enumerate(rows):
        print "\t%d: %s %s [%s] [id %d, root %d]" % (idx,row['pos'],row['eng'],row['pdef'],row['id'],row['stem'])
      answer = raw_input("\tWhich word to link?")
      stems.append(rows[int(answer)]['stem'])
    elif (len(rows)==0):
      print "FATAL: %s has 0 matches." % word
      sys.exit(0)
    else:
      row = rows[0]
      stems.append(row['stem'])

  lower=min(stems[0],stems[1])
  higher=max(stems[0],stems[1])
  print "Need to link %s and %s" % ( lower, higher ) 
  update = """insert into cf (a,b) values (%s,%s)""" % (lower,higher)
  try:
    #print update
    c.execute(update)
    if (c.rowcount):
      print update
  except _mysql_exceptions.IntegrityError, e:
    print "Insert error: %s" % e

def main():
  (db,c) = belau.connect()

  inputfile='words.txt'
  for line in codecs.open(inputfile):
    db.commit()
    line = line.decode('utf-8').strip()
    line = line.replace('’', "'")
    entered = False
    parts = line.split('--')
    pieces = parts[0].split()
    if (pieces[0] == 'w' or pieces[0] == 'v'):
      wid = root_word(pieces,c)
      if pieces[0] == 'v':
        add_perfectives(c,parts[1],wid)
        del parts[1]
      for part in parts[1:]:
        add_branch(c,part,wid)
    elif (pieces[0] == 'l'):
      add_link(c,pieces[1],pieces[2])
    else:
      pieces = parts[0].split()
      type = pieces[0]
      del pieces[0]
      pal = ' '.join(pieces)
      eng = parts[1]
      print "\tPhrase or example %s: %s -> %s" % (type,pal,eng)
      if (type=='p'):
        add_word(c,pal,'expression',eng,wid)
      elif (type=='e'):
        add_example(c,pal,eng,wid)
      else:
        print "FATAL error.  Unrecognized entry %s" % line
        sys.exit(0)
    continue

  # commit and close
  db.commit()
  c.close()
  db.close()
    
if __name__ == "__main__": main()


