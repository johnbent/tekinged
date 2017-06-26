#! /usr/bin/env python

import sys

# the last 1-2 characters in stem help determine whether optional e is needed
def optional_e(stem):
  if (stem[-2:] == 'ch'): return 'e'
  if (stem[-1:] == 'r'):  return 'e'
  return ''

def convert(p3s):
  stem=p3s[:-2]
  suffix=p3s[-2:]
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
  return (p1s,p2s,p3s,p1pi,p1pe,p2p,p3p)


def main():
  sys.argv.pop(0) # remove the executable name 
  for arg in sys.argv:
    forms = convert(arg)
    print forms


if __name__ == "__main__": main()

