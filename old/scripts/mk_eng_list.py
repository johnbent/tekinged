#! /usr/bin/env python

import sys
import pymysql
import string
import re
import os

def main():
  try:
    password = sys.argv[1];
  except IndexError:
    print "Usage: %s password" % sys.argv[0]
    return 
  db=pymysql.connect(user="johnbent",passwd=password,db="belau",host="mysql.tekinged.com")
  c=db.cursor()

  distinct = set()

  c.execute("""select eng from all_words3 where length(eng) > 0 and pos not like 'var.'"""); 
  for row in c.fetchall():
    clean = re.sub('e.g.',' ', row[0])
    clean = re.sub(' +',' ',clean)
    clean = re.sub('[%s]' % re.escape(string.punctuation), ' ', clean)
    words = clean.split(' ') 
    distinct.update(words)

  # somehow a blank word is added 
  distinct.remove('')

  #f = open('output.txt', 'w')
  #f.write('\n'.join(sorted(distinct)))
  #f.close()

  #c.execute("""drop table if exists `eng_list`""");
  #c.execute("""create table `eng_list` ( `eng` varchar(32) NOT NULL DEFAULT '' )""");
  #c.execute("""LOAD DATA LOCAL INFILE 'output.txt' INTO TABLE `eng_list`""")
  #os.unlink('output.txt')
  #sys.exit(0)

  values= "('" + "'),('".join(sorted(distinct)) + "')"
  c.execute("""drop table if exists `eng_list`""");
  c.execute("""create table `eng_list` ( `eng` varchar(32) NOT NULL DEFAULT '' )""");
  q = "insert into `eng_list` (`eng`) values %s" % values
  print q
  c.execute(q)
  db.commit()
  c.close()
  db.close()
  sys.exit(0)

  c.execute("""drop table if exists `eng_list`""");
  c.execute("""create table `eng_list` ( `eng` varchar(32) NOT NULL DEFAULT '' )""");
  for w in sorted(distinct):
    if (len(w)):
      q = "insert into `eng_list` (`eng`) values ('%s')" % w
      print q
      c.execute(q)
  #print sorted(distinct) 
  #print len(distinct)

  # commit and close
  db.commit()
  c.close()
  db.close()

if __name__ == "__main__": main()


