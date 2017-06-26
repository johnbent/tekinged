#! /bin/env python

import csv
import pymysql
import argparse
import sys
import glob

sys.path.append('/Users/bentj/Dropbox/belau/scripts')
import belau

parser = argparse.ArgumentParser(description='Add phrases to the belau db')
parser.add_argument('-s', action="store", dest="s", type=int)
args = parser.parse_args()

# get a db connection
(db,c) = belau.connect()

inserts=0
for file in glob.glob("Batch_*.csv"):
  print "Processing %s" % file
  f = csv.DictReader(open(file))
  fields=f.fieldnames
  table=list(f)
  for row in table:
    placeholders = ', '.join(['%s'] * len(row))
    columns = ', '.join(row.keys()).replace('.','_')
    sql = "INSERT IGNORE into %s ( %s ) VALUES ( %s )" % ('mturk', columns, placeholders)
    #print "%s" % sql
    c.execute(sql, row.values())
    print "%s -> %d" % (row['HITId'],c.rowcount)
    inserts += c.rowcount

print "%d rows inserts" % inserts
db.commit()
db.close()
