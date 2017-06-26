#! /usr/bin/env python

# http://boto.readthedocs.org/en/latest/ref/mturk.html

from boto.mturk.connection import MTurkConnection
from boto.mturk.price import Price 
from pprint import pprint
import pymysql
import datetime
import myturk2 as myturk

bonuses = []
 
ACCESS_ID ="AKIAIRZ5JZ2KFCLKU4MQ"
SECRET_KEY = "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"
HOST = 'mechanicalturk.amazonaws.com'
HOST = 'mechanicalturk.sandbox.amazonaws.com'
 
mtc = MTurkConnection(aws_access_key_id=ACCESS_ID,
                      aws_secret_access_key=SECRET_KEY,
                      host=HOST)


def cents_to_dollars(num_cents):
    return round(num_cents/100.0,2)

def bonus(mtc,worker_id,assignment_id,bonus,reason):
  if (worker_id not in bonuses):
    print "Will bonus %s (%s) to %s" % (bonus, Price(cents_to_dollars(bonus)),worker_id)
    mtc.grant_bonus(
      worker_id=worker_id,
      assignment_id=assignment_id,
      bonus_price=Price(cents_to_dollars(bonus)),
      reason=reason)
    bonuses.append(worker_id)

def disable_hit(mtc,hit):
  print "Disable old Hit %s: %s"  % ( hit.HITId, hit.Title )
  mtc.disable_hit(hit.HITId)
 
def get_hits(mtc,only_reviewable=False):
    page_size = 50
    if (only_reviewable):
      hits = mtc.get_reviewable_hits(page_size=page_size)
    else:
      hits = mtc.search_hits(page_size=page_size)
    print "Total results to fetch %s " % hits.TotalNumResults
    print "Request hits page %i" % 1
    total_pages = float(hits.TotalNumResults)/page_size
    int_total= int(total_pages)
    if(total_pages-int_total>0):
        total_pages = int_total+1
    else:
        total_pages = int_total
    pn = 1
    while pn < total_pages:
        pn = pn + 1
        print "Request hits page %i" % pn
        if (only_reviewable):
          temp_hits = mtc.get_reviewable_hits(page_size=page_size,page_number=pn)
        else:
          temp_hits = mtc.search_hits(page_size=page_size,page_number=pn)
        hits.extend(temp_hits)
    return hits

def insert_mys():
  print "noop"
  #pal = clean_str(assignment.answers[0][0].fields[0])
  #eng = clean_str(assignment.answers[0][1].fields[0])
  #des = clean_str(assignment.answers[0][2].fields[0])
  #query = 'INSERT INTO mcknight (palauan,english,explanation,id,mturk_id) VALUES (%s,%s,%s,%s,%s)' 
  #try:
  #  c.execute(query,(pal,eng,des,which_proverb,worker))
  #except pymysql.err.IntegrityError, e:
  #  print "Insert failed: %s" % e

hits = get_hits(mtc)

db=pymysql.connect(user="johnbent",passwd="0730Remliik",db="belau",host="mysql.tekinged.com")
c=db.cursor()
 
for hit in hits:
    def clean_str(string):
      string = string.replace('\r\n', ' ').replace('\n', ' ').replace('\r', '').replace('  ',' ').replace('- ','')
      return string

    hitid = hit.HITId
    title = hit.Title
    dict_page = title.rsplit(None, 1)[-1] 
    desc = hit.Description

    # disable all the previous results that weren't the new scrape hits
    if (title.find('Scrape') == -1):
      disable_hit(mtc,hit)
      continue

    hit_str=myturk.display_hit(hit,True)
    ass_str=myturk.list_assignments(hitid,mtc)
    print hit_str
    print ass_str
    assignments = mtc.get_assignments(hit.HITId)
    if (len(assignments) != 2):
      print "Oh shit, %d did not get 2 results" % hit.HITId
      sys.exit(0)
    results = list()
    for assignment in assignments:
        status = assignment.AssignmentStatus
        worker = assignment.WorkerId
        #pprint( dir(assignment) )
        result = assignment.answers[0][0].fields[0]
        print "Dictionary page #%s : %s, %s, %s, %s" % (dict_page, hitid, title, worker, status)
        results.append(result)
        #bonus(mtc,worker,assignment.AssignmentId,30,"I heard these were harder than I intended.  Sorry and thanks.")
        if (status == 'Submitted'):
          mtc.approve_assignment(assignment.AssignmentId)
    if (len(results) != 2):
      print "Oh shit, %d did not get 2 results" % hit.HITId
      sys.exit(0)
db.commit()
db.close()
