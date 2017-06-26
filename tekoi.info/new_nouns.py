#! /usr/bin/env python

import sys
import pymysql

def insert(c,db,pal,pos,eng,stem):
  if (stem!=0):
    query = "insert into all_words3 (pal,pos,eng,stem) values (%s,%s,%s,%s)"
    values = (pal,pos,eng,stem)
  else:
    query = "insert into all_words3 (pal,pos,eng) values (%s,%s,%s)"
    values = (pal,pos,eng)
  try:
    print "Execute %s %s?" % (query, values)
    var = raw_input("y|n? ")
    if (var != 'n'):
      c.execute(query,values)
      rid=c.lastrowid
      if (stem==0):
        #print "Updating stem for root %s" % pal
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

def search(c,word,pos):
  c.execute("""select id,pos,eng,stem from all_words3 where pal like '%s' and pos rlike '%s'""" % (word,pos))
  rows = c.fetchall()
  return rows

def main():
  db=pymysql.connect(user="johnbent",passwd="0730Remliik",db="belau",host="mysql.tekinged.com")
  c=db.cursor()

  # a few possible cases
  # 1. Neither base or poss.3s are in tekinged.com
  # 2. Word is [n.oblig.poss.] and poss.3s is not in tekinged.com
  # 3. Base is in but poss.3s is no
  # 4. Base is missing but poss.3s is in there

  f = open('nouns.txt')
  for line in f.readlines():
    words=line.split()
    base=words[0]
    poss=words[-5] 
    eng=' '.join(words[1:-7]) 
    if (base != '[n.oblig.poss.]'):
      # handles cases 1 and 4
      rows = search(c,base, 'n.')
      if (len(rows)==0):
        print "Inserting %s %s" % (base,eng)
        stem=insert(c,db,base,'n.',eng,0)
        rows = search(c,poss,'n.poss.3s')
        if (len(rows)==0):
          print "Inserting %s as poss of %s (%d)" % ( poss,base,stem )
          insert(c,db,poss,'n.poss.3s','',stem)
        else:
          print_rows(rows,poss,'')
        var = raw_input("Press enter to continue: ")
      else:
        prows = search(c,poss,'n.poss.3s')
        if (len(rows)==1 and len(prows)==0):
          stem=rows[0][0]
          print "Adding %s to %s: %s" % (poss,base,eng)
          if (eng != rows[0][2]):
            print "Update %s?" % base
            print "\tNew: %s\n\tOld: %s" % (eng,rows[0][2])
            var = raw_input("y|n?")
            if (var == 'y'):
              q = "update all_words3 set eng=%s where id=%s" 
              c.execute(q,(eng,rows[0][0],))
          insert(c,db,poss,'n.poss.3s','',stem)
        else:
          pass
        #print_rows(rows,base,poss)
    else:
      # handles case 2
      rows = search(c,poss,'n.poss.3s')
      if (len(rows)==0):
        print "Insert %s as its own stem: %s?" % ( poss,eng )
        var = raw_input("Press enter to continue: ")
        if (var != 'n'):
          stem=insert(c,db,poss,'n.poss.3s',eng,0)
        else:
          print "Did not insert"
      else:
        pass
      
  sys.exit(0)
  
  stems = [] 
  linkable = True

  for word in ( a , b ):
    if word.isdigit():  # might already be the ids
      stems.append(word)
      continue
    c.execute("""select id,pos,eng,stem from all_words3 where pal like '%s'""" % word)
    rows = c.fetchall()
    if (len(rows)!=1):
      print "%s has %d matches" % (word, len(rows))
      linkable=False 
      for row in rows:
        print "\t%s %s %s %s %s" % (word, row[0], row[1], row[2], row[3])
    else:
      row = rows[0]
      if (row[0] != row[3]):
        linkable=False
        print "Sorry. Not linkable: %s is not a root word (%s != %s)" % (word, row[0], row[1])
      else:
        stems.append(row[0])

  if (linkable == False):
    print "Sorry.  Not linkable."
    sys.exit(0)

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

  # commit and close
  db.commit()
  c.close()
  db.close()
    
if __name__ == "__main__": main()


