def plotWarp(a,b,warpObj, ts=[]):
	'''Plots the comprehensive results of a time warp, including the 
	cost matrix, backtrace path, visualisation of the warping statistics and the 
	individual time series, with warp lines.

	Parameters
	----------
		a : list
			First time series, which has been warped against time series b
		b : list 
			Second time series (reference)
		warpObj : dict
			A timeWarpOB warp object - see output of ``timeWarpOB.timeWarp()``.
			NB: the object must contain the calclauted cost matrix (i.e. ``retMat = True``)
		ts : list
			Optional list of timestamps for displaying on the graphs. If no timestamps are 
			given, each time period will be given an incremented number, staring at 1.

	Returns
	-------
		matplotlib.pyplot
			A composite plot showing the results of the time warp.

	'''

	import matplotlib.pyplot as plt

	costMat = warpObj["costMat"]
	path = warpObj['backTracePath']
	w = warpObj['warpWindow']

	n = len(costMat)
	gridSize=(5,5)

	#If no timestamps, use period values
	if ts == []:
		dateRot = 0
		for i in range(n):
			ts.append(i)
	else:
		dateRot = 20

	# Main warp path plot (centre)
	plt.subplot2grid(gridSize, (2,1), rowspan=2, colspan=2)

	plt.imshow(costMat, interpolation='nearest', cmap='Greys',aspect='auto') 
	plt.autoscale(False)
	plt.gca().invert_yaxis()
	plt.xlabel("b")
	plt.ylabel("a")
	plt.plot([0,n], [0,n], 'y')
	plt.plot([0,n-w], [w,n], 'm--')
	plt.plot([w,n], [0,n-w], 'm--')
	for i in range(len(path)-1):
		x1 = path[i][1]
		x2 = path[i+1][1]

		y1 = path[i][0]
		y2 = path[i+1][0]

		plt.plot([x1,x2], [y1,y2], 'r')


	# Lower time series plot (series b)
	plt.subplot2grid(gridSize, (4,1),colspan=2)
	plt.plot(ts,b, 'g^-' ,label='b')
	plt.xticks(rotation=dateRot)

	# Left time series plot (series a)
	c = a.copy()
	plt.subplot2grid(gridSize, (2,0),rowspan=2)
	plt.plot(c,ts, 'bo-' ,label='a')
	plt.gca().invert_xaxis()

	# Both time series with tie-lines
	plt.subplot2grid(gridSize, (0,1), rowspan=2, colspan=2)
	plt.plot(ts, a, 'bo-' ,label='a')
	plt.plot(ts, b, 'g^-', label ='b')
	plt.legend();
	for [map_x, map_y] in path:
		plt.plot([ts[map_x], ts[map_y]], [a[map_x], b[map_y]], 'r')
	plt.xticks(rotation=dateRot)

	# Rotated warping plot
	plt.subplot2grid(gridSize, (2,3), rowspan=2, colspan=2)
	xMax = len(a)
	yMin = -(w) - 1
	yMax = (w) + 1
	avgWarp = warpObj['warpStats']['avgWarp']

	plt.plot([0,xMax], [0,0], 'y')
	plt.plot([0,xMax], [-(w),-(w)], 'm--')
	plt.plot([0,xMax], [w,w], 'm--')
	plt.plot([0,xMax],[avgWarp,avgWarp], 'c:')

	plt.axis([0,xMax, yMin,yMax])
	plt.gca().set_autoscale_on(False)
	for i in range(len(path)-1):
		i1 = path[i][0]
		i2 = path[i+1][0]
		j1 = path[i][1]
		j2 = path[i+1][1]

		x1 = (i1 / 2) + (j1 / 2)
		y1 = (i1) - (j1)

		x2 = (i2 / 2) + (j2 / 2)
		y2 = (i2) - (j2)

		plt.plot([x1,x2], [y1,y2], 'r')

	plt.tight_layout(pad=0.4, w_pad=0.4, h_pad=0.4)

	plt.show(block=False);


def plotSeries(a,b,path):
	'''Plots the two time series with warp lines as a single plot

	Parameters
	----------
		a : list
			First time series, which has been warped against time series b
		b : list 
			Second time series (reference)
		warpObj : dict
			A timeWarpOB warp object - see output of ``timeWarpOB.timeWarp()``.

	Returns
	-------
		matplotlib.pyplot
			A single plot showing the warp lines on the two time series.
	'''

	import matplotlib.pyplot as plt

	path = warpObj["backTracePath"]

	plt.plot(a, 'bo-' ,label='x')
	plt.plot(b, 'g^-', label = 'y')
	plt.legend();
	for [map_x, map_y] in path:
		plt.plot([map_x, map_y], [a[map_x], b[map_y]], 'r')
	plt.show(block=False)