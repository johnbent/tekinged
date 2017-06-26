#! /usr/bin/env python

import os
import pyglet
import glob
import time
import sys

sys.path.append('/Users/bentj/Dropbox/belau/scripts')
sys.path.append('../scripts')
import belau

def play(player,src):
  try:
    #music = pyglet.resource.media(src)
    music = pyglet.media.load(src, streaming=False)
    music.play()
    time.sleep(1)
    ans = raw_input("\tWas this sound good (r to replay, q to quit)? [y|n|r|q]: ")
    if (ans == 'r'):
      return play(player,src)
    if (ans == 'q'):
      sys.exit(0)
    else:
      success = (ans == 'y')
  except pyglet.media.avbin.AVbinException, e:
    print "Exception playing file. Assuming bad."
    success = 0  
  print "%s -> %d" % ( src, success )
  return success

def get_table():
  return "upload_audio"

def get_filter(dbid):
  return "where externalid=%d and externaltable='examples' and externalcolumn='palauan'" % dbid

def get_sentence(c,dbid):
  q = "select id,pal,verified,uploaded from %s %s" % (get_table(), get_filter(dbid))
  c.execute(q)
  rows = c.fetchall()
  assert(len(rows)==1)
  return (rows[0]['pal'],rows[0]['verified'],rows[0]['uploaded'])

def verify(c,dbid,success):
  print "%s %d" % (( "Validating" if success==1 else "Invalidating"), dbid)
  q = "update %s set verified=%d,uploaded=%d %s" % (get_table(),success,success,get_filter(dbid))
  c.execute(q)

def setup_pyglet()
  working_dir = os.path.dirname(os.path.realpath('.'))
  pyglet.resource.path = [os.path.join(working_dir,'examples.palauan')]
  pyglet.resource.reindex()

def main():
  setup_pyglet()

  (db,c) = belau.connect()
  for file in list(glob.glob('*.mp3')):
    dbid = int(os.path.splitext(file)[0])
    (pal,verified,uploaded) = get_sentence(c,dbid)
    if ((uploaded == 1 and verified == 1) or uploaded==0):
      print "## Skipping %s" % (pal)
      continue  # this one is good
    print "## Checking %d [%s]" % (dbid,pal)
    success = play(None,file)
    verify(c,dbid,success)
    db.commit()

if __name__ == "__main__":
  main()
