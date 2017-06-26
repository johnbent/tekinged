import numpy
import scipy
import scipy.optimize
import scipy.stats

from Shared import *

class Fitter:
	""" 
		Convenient functions for fitting
	"""
	
	def __init__(self, f, initial_params):
		self.__dict__.update(locals())
	
	def negative_ll(self, params, freqs, ranks):
		""" Fitting by negative log token likelhood """
		#print params,  sum( freqs * self.f(params, ranks) )
		assert min(freqs) > 0.0, "Counts must be nonzero! (added 2013 Aug 26)"
		return -sum( freqs * log( self.f(params, ranks) ) ) # compute the log likelihood
	
	def fit(self, freqs, ranks, initial_params=None):
		"""
			Returns the fit parameters and the fitted values
		"""
		self.fitted = scipy.optimize.fmin(self.negative_ll, numpy.array(self.initial_params if initial_params is None else initial_params), args=(freqs, ranks) )
		return [self.fitted, self.negative_ll(self.fitted, freqs, ranks), self.f(self.fitted, ranks)]
		