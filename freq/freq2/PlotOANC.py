
import matplotlib.pyplot as plt

import random, itertools
from Shared import *
from Fitter import *

anc = load_counts("Counts/anc-counts.txt")
words, freqs, ranks =  freqdict2wordsfreqsranks(anc, random_split=True)

#############################################################
## Standard Zipf plot
#############################################################

fig = plt.figure(num=None, figsize=(10,10))
sp = fig.add_subplot(111)
myZipfPlot(sp, freqs, ranks, words=(words if len(words)<50 else None)) # plot names if not many words

sp.tick_params(axis='both', which='major', labelsize=20)
sp.set_xlabel(r"$Log_e$ frequency rank", size=23)
sp.set_ylabel(r"$Log_e$ normalized frequency", size=23)

plt.savefig("Zipf-Oanc.pdf")#, dpi=400)

#############################################################
##And do a residual plot
#############################################################

fig = plt.figure(num=None, figsize=(10,10))
sp = fig.add_subplot(111)
probs = numpy.array(freqs, dtype=float) / sum(freqs)
phat, obj, z = ZIPF_MANDELBROT.fit(freqs, ranks) 
print phat, obj

log_error = log(z) - log(probs)
	
x=log(ranks)
y=log_error
gridsize=150
sp.hexbin(x, y, gridsize=gridsize, cmap='winter', reduce_C_function=numpy.sum, mincnt=1, bins='log', alpha=0.7)

sp.plot([0,max(log(ranks))], [0,0], c='red', lw=5.0 ) # add a horizontal line

# Fix this plot margins. NOTE: THIS TRIMS SOME OF THE Y VALUES ON THE RHS
sp.axis([x.min()-1, x.max()+1,-1., 1.])

sp.tick_params(axis='both', which='major', labelsize=20)
sp.set_xlabel(r"$Log_e$ frequency rank", size=23)
sp.set_ylabel("Error (log space)", size=23)

plt.savefig("Zipf-Oanc-err.pdf")#, dpi=400)

# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
# Make the plot of Zipf and residuals
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

print  "# The log error correlation:", scipy.stats.spearmanr( ranks, log_error)
print  "# The log error correlation (first 1k):", scipy.stats.spearmanr( ranks[ranks<1000], log_error[ranks<1000])

# Do an autocorrelation:

from pypr.stattest.ljungbox import *
import scipy.stats

#http://pypr.sourceforge.net/stattest.html
for  till in [25, 50, 100, 1000, len(log_error)] :
	
	#print log_error[:till]
	h, pV, Q, cV = lbqtest(log_error[:till], range(1, 10), alpha=0.1)
	print '\tlag   p-value          Q    c-value   rejectH0'
	for i in range(len(h)):
		print till, "%-2d %10.3f %10.3f %10.3f      %s" % (i+1, pV[i], Q[i], cV[i], str(h[i]))
	

print "==============================="
#import pypr.stattest
#print jungbox(log_error, range(1,100), alpha=0.1)
#print  "# Durbin-watson log error:", durbin_watson( log_error )
#print  "# Durbin-watson relative error:", durbin_watson( relative_error )


quit()
