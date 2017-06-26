import numpy


def LocallySmoothedRegression(x,y, newx, h=1.0):
	"""
		Do a locally smoothed regression with x,y, predicting newx,newy
		#http://sfb649.wiwi.hu-berlin.de/fedc_homepage/xplore/ebooks/html/csa/node149.html
	"""
	assert len(x)==len(y)
	
	def W(d): return (1.-d**2.0)**2.0 if abs(d) < 1. else 0.0 # bisquare function
	
	x = numpy.array(x)
	y = numpy.array(y)
	newx = numpy.array(newx)
	
	newy = []
	for nxi in newx:
		
		# vector of weights for each x
		weights = numpy.array( map(lambda xi: W((nxi-xi)/h), x) )
		weights = weights / sum(weights)
		
		newy.append( sum(weights*y) )
		
	return newx, newy
	