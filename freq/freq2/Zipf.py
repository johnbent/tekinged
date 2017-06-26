
import matplotlib.pyplot as plt

import random, itertools
from Shared import *
from Fitter import *

# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
# Make the OLD style zipf, with badness
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

anc = load_counts("Counts/anc-counts.txt")
words, freqs, ranks =  freqdict2wordsfreqsranks(anc, random_split=True)
probs = map(float, freqs) / sum(freqs)

myZipfPlot(plt, freqs, ranks)
	
print "# Doing local regression "

newx = numpy.array(xrange(len(probs)))+1

newx, newy = locally_smoothed_regression( log(ranks), log(probs), log(newx), h=1.0 )
print newx
print newy
plt.plot( newx, newy, color="black")

print "# Saving "
plt.savefig("zipf.pdf", dpi=400)
plt.show()

#quit()

#plt.plot( log(ranks), log(z), c='red' 

# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
# Make the plot of Zipf and residuals
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

words, freqs, ranks =  load_text(INPUT_TEXT_NAMES)
probs = freqs / sum(freqs)

phat, obj, z = ZIPF_MANDELBROT.fit(freqs, ranks) 

log_error = log(z) - log(probs)
relative_error = log(z) / log(probs)

# Plot two error measures
plt.subplot(1,2,1)
plt.plot( log(ranks), log(probs), c='blue', lw=0, marker='.' )
plt.plot( log(ranks), log(z), c='red' )

plt.subplot(1,2,2)
plt.scatter( log(ranks), log_error, lw=0, alpha=1, marker="." )
plt.ylim([-1, 1])
plt.plot([0,max(log(ranks))], [0,0], c='black', lw=0.4)

plt.savefig("err.png", dpi=500)

print  "# The log error correlation:", scipy.stats.spearmanr( ranks, log_error)
print  "# The log error correlation (first 1k):", scipy.stats.spearmanr( ranks[ranks<1000], log_error[ranks<1000])
print  "# The relative error correlation:", scipy.stats.spearmanr( ranks, relative_error)
print  "# The relative error correlation (first 1k):", scipy.stats.spearmanr( ranks[ranks<1000], relative_error[ranks<1000])

print  "# Durbin-watson log error:", durbin_watson( log_error )
print  "# Durbin-watson relative error:", durbin_watson( relative_error )


#quit()

# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
# Plot the measure with params fit over different subsets of words
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

#words, freqs, ranks = load_text(INPUT_TEXT_NAMES)

#starts, phats = [], []

#step = 500
#for start in xrange(0, len(words), step):
	
	#stop = start+step
	#phat, obj, z = ZIPF_MANDELBROT_EXP.fit(freqs[0:stop], ranks[0:stop]) ## TODO: HERE maybe we start at 0 or start at "start"?
	
	#phats.append(phat.tolist())
	#starts.append(start)

#params = zip(*phats) # unzip
#for j, p in enumerate(params):
	#plt.subplot(1,len(params),j+1)
	#print j, p
	#plt.plot( starts, p, c='blue', lw=1, alpha=1 )

#plt.savefig("param-fits.png", dpi=500)

#quit()

# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
# Plot the corpus separating other types, with permutation
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~


sepcolors = { ' ': 'black', 'e': 'blue', 't': 'yellow', 'a': 'green', 'o': 'red', 'i': 'purple' }
for sep, color in sepcolors.items():

	words, freqs, ranks = load_text(INPUT_TEXT_NAMES, sep=sep, top=5000, permute_wordforms=True)
	probs = freqs / sum(freqs)

	plt.scatter( log(ranks), log(probs), marker=".", c=color, lw=0, alpha=1 )

	#phat, obj, z = ZIPF_MANDELBROT.fit(freqs, ranks)
	#plt.scatter( log(ranks), log(z), lw=0, alpha=1.0, marker=".", c=color)

plt.savefig("o.png", dpi=500)

quit()
