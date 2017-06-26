#! /usr/bin/env python

import belau
import sys
import pymysql

def main():
  db=pymysql.connect(user="johnbent",passwd="chemelekelbuuch",db="belau",host="mysql.tekinged.com")
  c=db.cursor()

  f = open('pdefs.txt')
  for line in f.readlines():
    entered = False
    pword,pdef = line.rstrip().split(' -- ')
    pword = pword.lower()
    #print "%s -> %s" % (pword, pdef)
    rows=belau.search(c,pword)
    if (len(rows)==0):
      print "\tWill insert %s -> %s" % (pword, pdef)
      belau.insert(c,db,None,pword,pdef,False)
      entered = True
    else:
      for row in rows:
        if (pdef == row[2]):
          #print "%s -> %s is already entered." % (pword,pdef)
          entered = True
    if (entered == False):
      print "Please specify where to enter %s -> %s" % (pword,pdef)
      idx = 0
      for idx, row in enumerate(rows):
          print "\t%d: Add to %s %s [%s]" % (idx,pword,row[1],row[2])
      nword = 'N' 
      skip  = 'S' 
      print "\t%s: As a new word" % nword 
      print "\t%s: Do not enter right now" % skip 
      answer = raw_input("Enter your choice: ")
      if (answer == nword):
        print "\tWill insert %s -> %s" % (pword, pdef)
        belau.insert(c,db,pword,pdef,False)
      elif (answer == skip):
        print "\tWill skip for now"
      elif (answer < nword):
        query = "update all_words3 set pdef=%s where id=%s"
        values = (pdef,rows[int(answer)][4],)
        print "\tWill query with %s %s" % (query, values)
        raw_input("Continue")
        c.execute(query,values)
        db.commit()
    continue
  sys.exit(0)

  # commit and close
  db.commit()
  c.close()
  db.close()
    
if __name__ == "__main__": main()


