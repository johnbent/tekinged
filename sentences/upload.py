#! /usr/bin/env python

import sys
import pymysql
import itertools
import MySQLdb
import argparse

sys.path.append('/Users/bentj/Dropbox/belau/scripts')
sys.path.append('../scripts')
import belau

parser = argparse.ArgumentParser(description='Upload sentences into the upload_sentence table.')
parser.add_argument('-w', action="store", default='Mar Ngiruchelbad', help='Who wrote the sentence.')
args = parser.parse_args()

def main():

  (db,c) = belau.connect()

  for line in sys.stdin:
    try:
      (pal,eng) = line.split('/')      
    except:
      print("error on line %s" % line)
      sys.exit(0)
    pal = MySQLdb.escape_string(pal.rstrip())
    eng = MySQLdb.escape_string(eng.rstrip())
    who = args.w

    update = """insert into upload_sentence (added,uploaded,assigned,assignee,submitted,pal,eng) 
              values (now(),1,now(),'%s',now(),'%s','%s')""" \
                  % (who,pal,eng)
    try:
      c.execute(update)
    except:
      print "Problem with mysql %s" % update
      sys.exit(0)

  # commit and close
  db.commit()
  c.close()
  db.close()
    
if __name__ == "__main__": main()


