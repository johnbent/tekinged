#! /bin/env python

from boto.mturk.connection import MTurkConnection
 
ACCESS_ID ="AKIAIRZ5JZ2KFCLKU4MQ"
SECRET_KEY = "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"
HOST = "mechanicalturk.sandbox.amazonaws.com"

mtc = MTurkConnection(aws_access_key_id=ACCESS_ID,
          aws_secret_access_key=SECRET_KEY,
          host=HOST)
           
print mtc.get_account_balance()
