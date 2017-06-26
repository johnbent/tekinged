#! /usr/bin/env python

import argparse
import fileinput
import os
import pymysql
import re
import string
import sys
import traceback

sys.path.append('/Users/bentj/Dropbox/belau/scripts')
sys.path.append('../scripts')
import belau
import synonyms

import frequency as f

def my_query(c,q,v=()):
  if args.q is True:
    print "#### %s" % q 
  return c.execute(q,v)

def find_missing(c):
  myfilter = "and pal like '%s'" % args.w if args.w is not None else ''
  mylimit = "limit %d" % args.l if args.l is not None else ''

  baseq = "from frequency where (isnull(eng) or isnull(pal) or isnull(pos) or isnull(vars))"; 
  my_query(c,"select count(*) %s" % baseq)
  print "Total words remaining to be processed: %d" % c.fetchone()['count(*)']
  
  q = "select * %s %s order by rand() %s" % (baseq,myfilter,mylimit);
  my_query(c,q)
  return c.fetchall()

# takes a stem from a missing frequency word and returns the corresponding word and word group from all_words3
def find_group(c,stem,combine=False):
  if combine is True:
    # only use words that haven't been matched yet
    q = "select a.stem from frequency a, frequency b where b.stem=%d and a.pal like b.pal and (isnull(a.pdef) or isnull(a.eng) or isnull(a.pos))" % stem
    #q = "select pal from frequency where stem=%d" % stem
    my_query(c,q)
    match = "("
    for row in c.fetchall():
      match += "a.id = %d or " % row['stem']
    match += "0)"
    q = "select distinct(b.id),b.* from all_words3 a, all_words3 b where b.stem=a.stem and %s" % match
  else:
    q = "select a.* from all_words3 a,all_words3 b where b.id=%d and a.stem=b.stem" % stem
  my_query(c,q)
  group = c.fetchall()
  groups = set()
  for g in group:
    groups.add(g['stem'])
    if g['id'] == stem:
      word = g
  return (word,group,len(groups)) 

# takes a word and a pdef and returns the pdef with XX for where the word should be
def get_pdef(word,variants,pdef):
  if pdef:
    #print variants, word
    #word = '|'.join([word]+variants)
    for word in (variants+[word]):
      pdef_re = re.compile(r'\b%s\b' % word, re.I)
      pdef = pdef_re.sub("XX", pdef) 
  else:
    return None
  return pdef

# gets all variants
def get_variants(w,group):
  variants = []
  variant_rows = []
  original = w

  # first, is w itself a variant or a contraction
  if w['pos'] == 'var.' or w['pos'] == 'cont.':
    for g in group:
      if g['pal'] == w['eng']:
        original = g
        variants.append(g['pal'])
        variant_rows.append(g)

  # now find all variants of the main word
  for g in group:
    if (g['pos'] == 'var.' or g['pos'] == 'cont.') and g['id'] != w['id'] and g['eng'] == original['pal']:
      variants.append(g['pal'])
      variant_rows.append(g)

  return (variants,variant_rows)

# takes a row from all_words3 
# and a set of rows for all the words in the group
# currently the row includes the word itself.
def find_word(w,group):
  homonyms = []
  original = w
  root = w

  # first find variants since we need them to produce the pdefs
  (variants,variant_rows) = get_variants(w,group)

  # put in the pdef for the word itself
  pdefs = [ get_pdef(w['pal'],variants, w['pdef']) ]

  if w['pos'] != 'var.':
    englishes = [ w['eng'] ]
    poses = [ w['pos'] ]
    original = w
  else:
    # ok, if w is a variant, find the original
    for g in group:
      if g['pal'] == w['eng']:
        original = g
        englishes = [ g['eng'] ]
        poses = [ g['pos'] ]
        pdefs.append(get_pdef(w['pal'],variants,g['pdef']))

  # now find all the homonyms and the root word
  for g in group:
    if g['pal'] == original['pal'] and g['id'] != original['id']:
      homonyms.append(g)
    if g['id'] == g['stem']:
      root = g

  # add pdefs for all the variants
  for v in variant_rows:
    pdefs.append(get_pdef(w['pal'],variants,v['pdef']))

  # add the info for any homonyms
  for h in homonyms:
    # if a homonym is someone a variant, then use its variant
    if h['pos'] == 'var.':
      for g in group:
        if g['pal'] == h['eng'] and g['pos'] != 'var.':
          h = g

    pdefs.append(get_pdef(w['pal'],variants,h['pdef']))
    poses.append(h['pos'])
    englishes.append(h['eng'])

  # now do the pos'es which we will need for the english if the english is missing
  pos = ",".join(set(filter(None,poses)))

  # if no english definition was found
  if len(filter(None,englishes)) == 0:
    englishes.append("%s of %s" % (pos,root['eng']))

  # if no pdef was found.
  if len(filter(None,pdefs)) == 0 and root['pdef'] is not None:
    #print "Adding missing pdef of %s" % root['pdef']
    #pdefs.append("%s er a %s" % (pos,get_pdef(w['pal'],variants,root['pdef'])))
    pass # becherei

  eng = " ".join(filter(None,englishes))
  pdef = " ".join(filter(None,set(pdefs)))
  alts = ",".join(filter(None,set(variants)))
  ori = original['origin']

  def print_kv(k,v):
    if v is not None:
      print "  %-4s: %s" % (k,v)

  print_kv('WORD',"%s %s [%s]" % (w['pal'].upper(),pos,alts))
  #print_kv('POS', pos)
  #print_kv('ALTS', alts)
  print_kv('ENG', eng)
  print_kv('PDEF',pdef)
  print_kv('ORIG',ori)
  return (eng,pos,pdef,alts,ori)


def add_synonyms(c,word):
  syns = set(raw_input("Add a list of synonyms : " ).split())
  #syns.add(word['pal'])
  synonyms.add_syns(c,syns,True)

def process(db,c,missing):
  for idx,m in enumerate(missing): 
    print "Word %4d/%4d %s " % (idx+1, len(missing), m['pal'])
    if process_word(c,m) is False:
      return
    else:
      db.commit() # commit every time to not lose work


def sort_group_cmp(x,y):
  # could use lambda to the sorted directly but we want a more complex thing with tie-breakers
  #for g in sorted(group,cmp=lambda x,y: cmp(x['pal'],y['pal'])):
  return cmp(x['pal'],y['pal']) if x['stem']==y['stem'] else cmp(x['stem'],y['stem'])

def process_word(c,m,combine=True,show_group=None):

  (word,group,group_count) = find_group(c,m['stem'],combine)

  if show_group is None:
    show_group = args.v

  if show_group is True:
    verbose = ""
    for g in sorted(group,cmp=sort_group_cmp):
      belau.print_from_row(g,'\t')
  else:
    verbose = " (v)erbose"
  (eng,pos,pdef,variants,origin) = find_word(word,group)
  query = "update frequency set eng=%s,pos=%s,pdef=%s,vars=%s,origin=%s where id=%s"
  ans = raw_input("Proceed [(y)es (e)nglish_only (r)efresh (q)uit s(Y)nonyms (s)kip%s%s]: " % 
      (" (c)ombine" if combine is False else " se(p)arate" if group_count>1 else "",verbose))

  # quit
  if ans == 'q':
    return False

  # go ahead and do the query
  elif ans == 'y' or ans == 'e':  
    if ans == 'e':
      pdef = ""
    my_query(c, query, (eng,pos,pdef,variants,origin,m['id'],))
    if combine is True:
      query = "delete from frequency where pal like '%s' and id != %d and isnull(pdef) and isnull(eng) and isnull(pos)" % (m['pal'],m['id'])
      my_query(c,query)
    return True

  elif ans == 'Y':
    add_synonyms(c,m)
    return process_word(c,m,combine)


  # refresh (because I've edited the database)
  elif ans == 'r':  
    return process_word(c,m,combine)

  # recurse to separate
  elif ans == 'p':  
    return process_word(c,m,False)

  # recurse to combine
  elif ans == 'c':  
    return process_word(c,m,True)

  # recurse to show the word-group
  elif ans == 'v':
    return process_word(c,m,combine,True)

  # skip this one
  elif ans == 's':  
    return True

  # unknown response, quit
  else:
    print "Unknown response %s.  Please try again." % ans
    return process_word(c,m,combine,show_group)

def parse_args():
  parser = argparse.ArgumentParser()
  parser.add_argument("-l", type=int, help="Only process l words.")
  parser.add_argument("-w", type=str, help="Only process particular word w.")
  parser.add_argument("-q", action="store_true", help="Show queries being executed.")
  parser.add_argument("-v", action="store_true", help="Verbose (show word groups.")
  #parser.add_argument("-d", help="show only one particular dln", type=str)
  #parser.add_argument("-c", help="Fetch DLN IT from CT", action="store_true")
  #parser.add_argument("-v", help="Show more info for each OID",action="store_true")
  #parser.add_argument("-s", help="Store the json to the CT",action="store_true") 
  global args
  args = parser.parse_args()

def main():
  parse_args()
  (db,c) = belau.connect()
  missing = find_missing(c)
  try:
    process(db,c,missing)
  except:
    e = sys.exc_info()[0]
    traceback.print_exc()
    print e
    print "Uh oh!  Exception.  Quitting and committing whatever progress we made"
  db.commit()
  c.close()
  db.close()
  sys.exit(0)

if __name__ == "__main__": main()


