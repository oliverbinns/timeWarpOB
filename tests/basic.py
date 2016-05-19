def sinCos(n=2):
	''' Generates a test dataset of sin and cosine over 200
	points in a time series.

	Parameters
	----------
		n : int
			Number of half-cycles to calculate the values over

	Returns
	-------
		x : list
			A list of sin(ts) values
		y : list
			A list of cos(ts) values
		ts : list
			A list of 'timestamp' values (radian angle values)
	'''
	import numpy as np

	ts = list(np.linspace(0, n*np.pi, 200))
	x = list(np.sin(ts))
	y = list(np.cos(ts))

	return x,y,ts

def testWarp(x,y,ts):
	''' Warps two time series, displays plots and prints 
		the warp statistics.

	Parameters
	----------
		x : list
			First time series, which has been warped against time series b
		y : list 
			Second time series (reference)
		ts : list
			Optional list of timestamps for displaying on the graphs. If no timestamps are 
			given, each time period will be given an incremented number, staring at 1.

	Returns
	-------
		matplotlib.pyplot
			A composite plot showing the results of the time warp.
		warpStats : dict
			Warp statistics (printed to the console only)
	'''
	import timeWarpOB as tw

	wo = tw.timeWarp(x,y)
	tw.plotting.plotWarp(x,y,wo)

	print(wo['warpStats'])