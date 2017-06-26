#! /usr/bin/env python

import sys
import pymysql

# the last 1-2 characters in stem help determine whether optional e is needed
def optional_e(stem):
  if (stem[-2:] == 'ch'): return 'e'
  if (stem[-1:] == 'r'):  return 'e'
  return ''


# takes a simple possessed noun (1ps, 2ps, 3ps, 1ppi) and returns the other forms 
def convert(noun):
  stem=noun[:-2]
  suffix=noun[-2:]
  vowel=suffix[:-1] 
  p1s  = stem+vowel+'k'
  p2s  = stem+vowel+'m'
  p3s  = stem+vowel+'l'
  p1pi = stem+vowel+'d'
  if(vowel is 'e'):
    p1pe = stem+"am"
    p2p  = stem+"iu"
    p3p  = stem+"ir"
  else:
    opt_e = optional_e(stem)
    p1pe = stem+opt_e+'mam'
    p2p  = stem+opt_e+'miu'
    p3p  = stem+opt_e+'rir'
  return ( ('1ps','2ps','3ps', '1ppi','1ppe','2pp','3pp'),
           ( p1s,  p2s,  p3s,   p1pi,  p1pe,  p2p,  p3p) )


def is_member(noun,members):
  for i in members:
    if i == noun:
      return True
  return False

def exceptional(noun):
  exceptions = [ 'chimal', 'blil', 'mlil', 'obengkel', 'chetil', 'bul', 'tul', 'til', 'ildisel' ]
  return noun in exceptions

def dont_expand(noun):
  only_p3s = [ 'tkul', 'bkul', 'kldelsel', 'surel', 'tengdel', 'kutelngal', 'deldekel', 'engedel' ]
  return noun in only_p3s

def main():
  try:
    password = sys.argv[1];
  except IndexError:
    print "Usage: %s password" % sys.argv[0]
    return 
  db=pymysql.connect(user="johnbent",passwd=password,db="belau",host="mysql.tekinged.com")
  c=db.cursor()

  # for every noun that has 3ps defined
  c.execute("""select 3ps from nouns where length(3ps)>0""")
  for row in c.fetchall():
    p3s=row[0]
    if dont_expand(p3s) or exceptional(p3s):
      print "Skipping %s" % p3s
      continue
    (schema,forms) = convert(p3s)
    for field,value in zip(schema,forms):
      #print "%s -> %s" % (field,value)
      update="""update nouns set %s='%s' where 3ps like '%s' and (isnull(%s) or length(%s)=0)""" % (field,value,p3s,field,field);
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
    
  # also do the command line args
  del sys.argv[0:2]
  for arg in sys.argv:
    forms = convert(arg)
    print forms


if __name__ == "__main__": main()


