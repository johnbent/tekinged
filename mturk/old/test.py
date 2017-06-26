#! /usr/bin/env python

import mturk3 as mturk

mconfig = {
  "use_sandbox" : False,
  "stdout_log" : True,
  "verify_mturk_ssl" : True,
  "aws_key" : "AKIAIRZ5JZ2KFCLKU4MQ",
  "aws_secret_key" : "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"
}

m = mturk.MechanicalTurk(mconfig)

r = m.request("GetReviewableHITs")
