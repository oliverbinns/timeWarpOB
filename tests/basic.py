# Tests (to be added)

def sinCos(n=2):
	''' Generates a test dataset of sin and cosine over 200
	points in a time series
	'''
	import numpy as np

	ts = list(np.linspace(0, n*np.pi, 200))
	x = list(np.sin(ts))
	y = list(np.cos(ts))

	return ts, x, y

def testWarp(x,y,ts):
	''' Warps two time series, displays plots and prints 
		the warp statistics
	'''
	import timeWarpOB as tw

	wo = tw.timeWarp(x,y)
	tw.plotting.plotWarp(x,y,wo)

	print wo['warpStats']