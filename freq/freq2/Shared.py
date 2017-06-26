from collections import defaultdict
import scipy
import scipy.stats
import numpy
import re
import os
import sys
from copy import copy, deepcopy
import random, itertools
from numpy import sum, log, exp, diff, sqrt
from Fitter import *
import csv
from matplotlib import cm
from LocallySmoothedRegression import LocallySmoothedRegression

try:			
    from scipy.misc import logsumexp
except ImportError:
    from scipy.maxentropy import logsumexp

def mystr(x): return '%.2f' % x

def mystar(p):
	if p<0.001: return '***'
	elif p<0.01: return '**'
	elif p<0.05: return '*'
	else:        return 'n.s.'
	
def load_counts(f):
	
	counts = dict()
	for word, c in csv.reader(open(f, 'r'), delimiter='\t', quotechar='"'):
		word = word.strip() # TODO: SHOULD NOT BE NEEDED ONCE WE'VE FIXED COMPUTE_WORD_COUNTS
		counts[word] = int(c)
		
	return counts
	
def list_files(directory, recurse=False, pattern=r"\.txt$", full_path=True):
	"""
		A generator to yield files of a certain type
	"""
	
	if recurse:
		for root, subFolders, files in os.walk(directory):
			for f in files:
				if re.search(pattern, f): 
					if full_path: yield os.path.join(root, f)
					else:         yield f
	else:
		for f in os.listdir(directory):
			if re.search(pattern, f): 
				if full_path: yield directory+"/"+f
				else:         yield f
			

def load_wordlists(files,collapse_case=True, pattern=r"\.txt$"):
	"""
		Load words in the files, skipping comments (anything after # on a line)
	"""
	word_lists = []
	if not isinstance(files, list): files = [files]
	
	for f in files:
		if not re.search(pattern, f): next
		words = set()
		#print ">>", f
		for k in open(f, 'r'):
			k = k.strip()
			if collapse_case: k = k.lower()
			k = re.sub(r"#.+$", "", k) # replace comments
			k = re.sub(r"\\s+", " ", k)
			if re.match("[a-zA-Z0-9]", k): # skip blank lines
				words.add(k)
		word_lists.append(words)
	return word_lists


def load_text(filenames, sep=" ", random_split=True, permute_wordforms=False, top=None, echo_to_tmp=True, remove_tags=False, small=False, vocabulary=None):
	"""
		This loads the filesnames by regex matching words, and then *recombining* them and then splitting by the split character.
		- sep - what should separate "words" (not necessarily a space, in some of our simulations)
		- random_split - should ranks and freqs be estimated separately? (via a binomial split)
		- permute_wordforms - if True, we shuffle up all the word forms (in-place in the corpus) before anything
		- top - only count the top this many words
		- echo_to_tmp - if True, we write to /tmp/load_text.txt the corpus as it looks (just for spot checking)
		- remove_tags - if True, we search and repalce things in < .. >, as in BNC
		- small - if true, we are debugging and we only use the first few

		Returns a list of freq, rank, word
	"""
	
	filenames = [f for f in filenames]
	if small: filenames = filenames[:50]
    
	# Load the actual corpus files
	corpus = ""
	for f in list(filenames):
		print "# Processing ", f
		for l in open(f, 'r'):
			l = l.strip().lower() # clean up
			if remove_tags: l = re.sub(r'<.*>', " ", l)
			
			corpus = corpus + " " + " ".join([x for x in re.findall("([a-z]+)", l)])
			
	corpus = re.sub("\\s+", " ", corpus) # clean up too many spaces
	
	# Restrict the vocaublary if we want
	if vocabulary is not None:
		corpus = " ".join(filter(lambda x: x in vocabulary, re.split(" ", corpus)))
	
	# If we permute wordforms, it means we shuffle around words and re-construct the corpus *before* we 
	# split things up. This lets us know if the real relationship between word lenght/frequency is what matters
	# in finding similar statistics
	if permute_wordforms:
		
		# construct a mapping
		word_types = list( set( re.split(" ", corpus) ) ) # using " " as a separator
		shuffled = copy.copy(word_types)	
		random.shuffle(shuffled) # shuffle this up
		
		fromto = dict() # build a mapping from -> to via the shuffling
		for f,t in zip(word_types, shuffled): fromto[f] = t
		
		# Now translate the corpus
		corpus = " ".join([ fromto[x] for x in re.split(" ", corpus) ])
		#print corpus
	
	# If we should dump a copy for perusal
	if echo_to_tmp:
		o = open("/tmp/load_text.txt", 'w')
		print >>o, corpus
		o.close()
		
	
	# Now we have the corpus, we may split it by whatever character we like and count the frequencies
	freq = defaultdict(int)
	for w in re.split(sep, corpus): 
		freq[w] += 1
	
	return freqdict2wordsfreqsranks(freq, random_split=random_split, top=top)


def freqdict2wordsfreqsranks(freq, random_split=True, top=None, toss_zeros=True, force_ranks=None):
	"""
		A helper to map a frequency diction to sorted words, freqs, ranks, with random splitting, and top, etc.  This also sorts by the ranks so that they are necessarily decreasing
		
		force_ranks - if not None, then we use the provided dict to compute the rank order. (NOTE: this disables random_split)
		
	"""
	# Now sort things
	si = sorted(freq.items(), key = lambda x: x[1], reverse=True)
	words, freqs = zip(*si) # this is how we unzip in python land (and other good lands)
	#print words, freqs
	
	freqs = numpy.array(freqs, dtype=int) # just convert types
	words = numpy.array(words, dtype=str)
	
	# Now trim -- NOTE: We do this before the binomial split
	if top is not None:
		freqs = freqs[0:top]
		words = words[0:top]
	
	# Now convert to ranks and split if necessary
	if force_ranks:
		ranks = numpy.array(rank( [force_ranks[w] for w in words], reverse=True))
	elif random_split:
		f_rank = numpy.random.binomial(freqs+1, 0.5)-1 # +1/-1 in order to allow random.binomial to deal with 0 
		freqs = freqs - f_rank # remove the samples for this
		ranks = numpy.array(rank(f_rank, reverse=True), dtype=int)
	else:
		ranks = numpy.array(rank(freqs, reverse=True), dtype=int)
		
	# Now order by ranks, making 0-indexed
	ranks, freqs, words = zip(* sorted( zip(ranks, freqs, words) ))
	
	freqs = numpy.array(freqs, dtype=int)
	words = numpy.array(words, dtype=str)
	ranks = numpy.array(ranks, dtype=int)
	
	if toss_zeros:
		selector = numpy.array(freqs>0, dtype=bool) & numpy.array(ranks>0, dtype=bool)
		words = words[selector] # toss bad ones
		freqs = freqs[selector]
		ranks = ranks[selector]
	
	return words, freqs, ranks
	
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
# Distribution functions:

# TODO: IF WE DO HELD_OUT, WE MUST FIX NORMALIZE SO THAT IT DOESN'T ONLY WORK ON THE FIT DATA -- THAT WOULD BE BAD
LINEAR                = Fitter( lambda p,R: normalize( p[0] + p[1]*R ), [1.0, -0.1] )
ZIPF                  = Fitter( lambda p,R: normalize( R**(-p[0]) ), [1.0] )
ZIPF_MANDELBROT       = Fitter( lambda p,R: normalize( (R+p[1])**(-p[0]) ), [1,0.0] )
ZIPF_MANDELBROT_PIECEWISE = Fitter( lambda p,R: normalize( (R+p[2])**(-p[1])*(R/len(R)<p[0]) +  (R*(1.0-p[0])+p[4])**(-p[3])*(R/len(R)>=p[0])  ), \
				[0.75, 1.0, 1.0, 1.0, 1.0] )
ZIPF_MANDELBROT_EXP  = Fitter( lambda p,R: normalize( (R+p[1])**(-p[0]) * exp(R * p[2] + p[3])  ), [1.0, 1.0, 0.00, 0.01] )
ZIPF_MANDELBROT_EXP2 = Fitter( lambda p,R: normalize( (R+p[1])**(-p[0]) * exp(R*R*p[4] + R * p[2] + p[3])  ), [1.0, 1.0, 0.00, 0.0, 0.0] )


## Common math
def normalize(z): return z/sum(z)
def lnormalize(z): return z - logsumexp(z)	
	
# From http://code.activestate.com/recipes/491268-ordering-and-ranking-for-lists/
def order(x, reverse=False):
	"""
	returns the order of each element in x as a list.
	"""
	z = itertools.izip(x, range(len(x)))
	z = itertools.izip(z, range(len(x))) #avoid problems with duplicates.
	return [ d[1] for d in sorted(z, reverse=reverse) ]
	
def rank(x, reverse=False):
	"""
	Returns the rankings of elements in x as a list.
	"""
	L = len(x)
	ordering = order(x, reverse=reverse)
	ranks = [None] * L
	for i in range(L):
		ranks[ordering[i]] = i + 1 # make 1-indexed
	return ranks

    
def durbin_watson(x):
	""" Compute durbin_watson """
	de = diff(x,1)
	return numpy.dot(de,de) / numpy.dot(x,x)

	
from matplotlib.colors import LinearSegmentedColormap


#http://matplotlib.1069221.n5.nabble.com/scatter-plot-individual-alpha-values-tt21106.html#none
class LinearColormap(LinearSegmentedColormap):
	def __init__(self, name, segmented_data, index=None, **kwargs):
	
		# If index not given, RGB colors are evenly-spaced in colormap.
		if index is None: index = numpy.linspace(0, 1, len(segmented_data['red']))
		
		# Combine color index with color values.
		for key, value in segmented_data.iteritems(): segmented_data[key] = zip(index, value)
		
		segmented_data = dict((key, [(x, y, y) for x, y in value]) for key, value in segmented_data.iteritems())
		LinearSegmentedColormap.__init__(self, name, segmented_data, **kwargs)
	
def myZipfPlot(plotter, freqs, ranks, gridsize=70, lw=5.0, smh=0.75,  probs=True, zmFit=True, smFit=True, words=None, margin=1.0, fontsize=20):
	"""
		A handly plotting function for my style Zipf plots.
	"""
	
	ranks = numpy.array(ranks, dtype=float)
	freqs = numpy.array(freqs, dtype=float)
	
	if probs: y = numpy.array(freqs, dtype=float) / sum(freqs)
	else:     y = freqs
	
	
	N = len(y)
	
	# To do variable alpha, we must use a colormap
	# Red for all values, but alpha changes linearly from 0.3 to 1
	#color_spec = {'blue':  [1.0, 0.20],'green': [0.0, 1.0], 'red':   [0.0, 0.0], 'alpha': [1.0, 1.0]}
	#alpha_blue = LinearColormap('alpha_blue', color_spec)
	
	x = log(ranks)
	y = log(freqs) - log(sum(freqs))
	
	#http://matplotlib.org/examples/pylab_examples/show_colormaps.html
	plotter.hexbin(x, y, gridsize=gridsize, cmap='winter', reduce_C_function=numpy.sum, mincnt=1, bins='log', alpha=0.7)
	plotter.axis([x.min()-margin, x.max()+margin, y.min()-margin, y.max()+margin])

	# Now do the Zipf-Mandelbrot fit
	if zmFit:
		phat, obj, z = ZIPF_MANDELBROT.fit(freqs, ranks) 
		plotter.plot( log(ranks), log(z), c='red', lw=lw, alpha=0.85 )
		print phat, obj
		
	if smFit:
		plotsmoothedx, plotsmoothedy = LocallySmoothedRegression(x,y, numpy.arange(min(x), max(x), (max(x)-min(x))/100.0), h=smh)
		plotter.plot( plotsmoothedx, plotsmoothedy, c='gray', lw=lw, alpha=0.85 )
		
		# and do one that aligns with the data for computing correlations
		_, smoothedy = LocallySmoothedRegression(x,y, sorted(x), h=smh)
	
	R=scipy.stats.pearsonr(log(z),log(freqs))
	
	if smFit:
		Rloess=scipy.stats.pearsonr(smoothedy,log(freqs))
		if Rloess[0] > R[0]:
			print "*** Warning: Loess explains less variance "+str(R[0])+"\t"+str(Rloess[0])
	else:
		Rloess = [1.0,1.0] # just ignore for now NOTE: This gives inaccurate R2adj
	
	# take min for R[0]/Rloess[0] to fix >1.0, due to small numerical error
	plotter.text( x.min(), y.min(), r'$\alpha='+ mystr(phat[0]) +r'$' + '\n' + \
					r'$\beta='+ mystr(phat[1]) +r' $' + '\n' + \
					r'$R^2='+ mystr(R[0]) +r' $ '+ mystar(R[1]) + '\n' + \
					r'$R_{adj}^2='+ mystr(min(R[0]/Rloess[0],1.0)) +r' $' + '\n', \
					fontsize=fontsize )                               
	