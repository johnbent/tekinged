#! /usr/bin/env python

from boto.mturk.connection import MTurkConnection
from pprint import pprint
import pymysql
 
ACCESS_ID ="AKIAIRZ5JZ2KFCLKU4MQ"
SECRET_KEY = "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"
HOST = 'mechanicalturk.amazonaws.com'
 
mtc = MTurkConnection(aws_access_key_id=ACCESS_ID,
                      aws_secret_access_key=SECRET_KEY,
                      host=HOST)

 
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
 
mtc = MTurkConnection(aws_access_key_id=ACCESS_ID,
                      aws_secret_access_key=SECRET_KEY,
                      host=HOST)
hits = get_hits(mtc)

db=pymysql.connect(user="johnbent",passwd="0730Remliik",db="belau",host="mysql.tekinged.com")
c=db.cursor()
 
for hit in hits:
    def clean_str(string):
      string = string.replace('\r\n', ' ').replace('\n', ' ').replace('\r', '').replace('  ',' ').replace('- ','')
      return string

    hitid = hit.HITId
    title = hit.Title
    which_proverb = title.rsplit(None, 1)[-1] 
    #print "Hit %s: %s"  % ( hit.HITId, hit.Title )
    #pprint( dir(hit) )
    assignments = mtc.get_assignments(hit.HITId)
    for assignment in assignments:
        status = assignment.AssignmentStatus
        worker = assignment.WorkerId
        #pprint( dir(assignment) )
        print "PROVERB #%s : %s, %s, %s, %s" % (which_proverb, hitid, title, worker, status)
        if (status == 'Submitted'):
          mtc.approve_assignment(assignment.AssignmentId)
          #pal=assignment.answers[0][0]
          #eng=assignment.answers[0][1]
          #des=assignment.answers[0][2] 
          #print "%s\n\t%s\n\t%s" % (dir(pal),dir(eng),dir(des)) 
          pal = clean_str(assignment.answers[0][0].fields[0])
          eng = clean_str(assignment.answers[0][1].fields[0])
          des = clean_str(assignment.answers[0][2].fields[0])
          query = 'INSERT INTO mcknight (palauan,english,explanation,id,mturk_id) VALUES (%s,%s,%s,%s,%s)' 
          try:
            c.execute(query,(pal,eng,des,which_proverb,worker))
          except pymysql.err.IntegrityError, e:
            print "Insert failed: %s" % e
          #print "%s\n\t%s\n\t%s\n" % (pal,eng,des)
          #for qf in assignment.answers[0]: 
            #print "%s" % qf.fields[0]
            #print "%s" % dir(question_form_answer.fields)
        #    print( "fields is type %s" % type(qf.fields))
#            for key, value in question_form_answer.fields:
#                print "%s: %s" % (key,value)
        #print "--------------------"
        mtc.disable_hit(hit.HITId)
db.commit()
db.close()
