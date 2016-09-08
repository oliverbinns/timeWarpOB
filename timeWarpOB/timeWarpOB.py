# Using numpy for matrix manipulations
import numpy as np

# Check if the numba module is installed (compiled, high-speed functions)
import importlib.util
foundNumba = importlib.util.find_spec("numba") is not None

if foundNumba:
	#Numba is installed, import @jit decorator
	from numba import jit
else:
	# Numba not installed, warn the user and make a blank @jit decorator
	def jit(f):
		'''Numba was not found in the current python environment
		'''
		return f


def timeWarp(a,b,method='DTW',window=0,retMat=True,**kwargs):
	'''This function is the main time warping interface, and acts
	as a convenient wrapper to the other functions.

	Parameters
	----------
		a : list or numpy 1D-array
			First time series, which will be compared against time series b
		b : list or numpy 1D-array
			Second time series (reference)
		method : str
			Time warping method ``{'DTW','ERP'}`` - see below
		window : int
			Time warping window constraint (default = 0)
		retMat : bool
			Whether to include the cost matrices in the returned object
		ERPg :	int
			g-value (for ``method = 'ERP'`` only)

	Returns
	-------
		warpObj : dict
			A timeWarpOB warp object, containing the following items:
		warpObj.backTraceCost : float
			The sum cost of following the backtrace through the cost matrix
		warpObj.backTracePath : list
			List or numpy array of pairs of coordinates in time-space describing the backtrace through
			the cost matrix
		warpObj.cost : float
			Bottom left value on the cost matrix.  With no warping window, this should 
			equal warpObj.backTraceCost
		warpObj.costMat : list
			A matrix (list of lists) or numpy array describing the cost matrix between the two time 
			series.  For a series of length n, this matrix will be of size n x n.  Only 
			output if ``retMat = True`` in the input parameters
		warpObj.distMat : list	
			A matrix (list of lists) or numpy array describing the L1-distance matrix between the two 
			time series.  For a series of length n, this matrix will be of size n x n.  
			Only output if ``retMat = True`` in the input parameters
		warpObj.warpWindow : int
			Returning the warp window parameter used (used by plotting functions)
		warpObj.warpStats : dict
			Warp statistics object, containing:		
		warpObj.warpStats.timeAhead : int
			The number of periods that time series a was in sync with time series b.
		warpObj.warpStats.timeAhead : int
			The number of periods that time series a was ahead of time series b.	
		warpObj.warpStats.timeBehind : int
			The number of periods that time series a was behind of time series b.	
		warpObj.warpStats.amountAhead : int
			The total sum of the number of periods that time series a was leading 
			time series b by.
		warpObj.warpStats.amountBehind : int
			The total sum of the number of periods that time series a was lagging
			time series b by.
		warpObj.warpStats.avgAhead : int
			Average amount of periods that a was ahead of a by, i.e. 
			amountAhead divided by timeAhead
		warpObj.warpStats.avgAhead : int
			Average amount of periods that a was behind b by, i.e. 
			amountBehind divided by timeBehind
		warpObj.warpStats.avgWarp : int
			Average amount of periods that a ahead or behind b by, i.e. 
			``(amountAhead - amountBehind) / (timeAhead + timeBehind + timeSync)``
			This will give positive values if a is on average ahead of b and negative
			values is a is on average behind b.

	Notes
	-----
	* If lists are supplied, the output matrices will be in list form.  If numpy arrays are supplied, the output will be as numpy arrays.

	* Numpy arrays will calculate faster, as no internal type conversion is required.

	* Time series should be of equal length.  If they are not, the longer will be clipped from the end.

	* ERP and DTW methods are available.  For information on how they work, see the module documentation.

	* Cost matricies should be returned for use by the plotting functions

	'''

	# Check if a list has been passed or numpy object
	usingList = False
	if type(a) == list:
		usingList = True
		a = np.array(a)

	if type(b) == list:
		usingList = True
		b = np.array(b)

	# Create a warp object to return
	warpObj = {}

	# Clip any longer time series
	minLen = min(len(a),len(b))
	a = a[0:minLen]
	b = b[0:minLen]

	# Get distance matrix
	dist = L1distances(a,b)
	
	# Get the cost matrix
	if method == 'DTW':
		costMat = DTWwarp(dist,a,b,w=window)
	elif method == 'ERP':
		ERPg = 0
		if 'ERPg' in kwargs:
			ERPg = kwargs['ERPg']
		costMat = ERPwarp(dist,a,b,w=window,g=ERPg)
	else:
		print("timeWarp error - incorrect warp method specified:", method)
		return -1

	# Extract the cost
	cIndex = len(costMat[0]) - 1
	cost = costMat[cIndex,cIndex]

	# Backtrace the warp path
	path, backTraceCost, warpStats = backTrace(costMat,dist)

	# Return the results
	if retMat == True:
		if usingList:
			warpObj["costMat"] = costMat.tolist()
			warpObj["distMat"] = dist.tolist()
		else:
			warpObj["costMat"] = costMat
			warpObj["distMat"] = dist
	
	warpObj["cost"] = cost
	warpObj["backTraceCost"] = backTraceCost
	warpObj["warpStats"] = warpStats

	if usingList:
		warpObj["backTracePath"] = path.tolist()
	else:
		warpObj["backTracePath"] = path
	
	if window == 0:
		warpObj["warpWindow"] = len(a)
	else:
		warpObj["warpWindow"] = window

	return warpObj


@jit
def L1distances(a,b):
	'''Calcluates the L1 distance matrix between two time series.

	Parameters
	----------
		a : list
			First time series, which will be compared against time series b
		b : list 
			Second time series (reference)

	Returns
	-------
		distance : list	
			A matrix (list of lists) describing the L1-distance matrix between the two 
			time series.  For a series of length n, this matrix will be of size n x n.  
	'''
	n = len(a)
	m = len(b)

	distance = np.zeros((n,m))

	for i in range(n):
		for j in range(m):
			distance[i,j] = abs(a[i] - b[j])

	return distance 

@jit
def ERPwarp(dist,x,y,w=0,g=0):
	'''Calcluates the ERP cost matrix between two time series.

	Parameters
	----------
		dist : list
			A matrix (list of lists) describing the L1-distance matrix between two 
			time series.  For a time series of length n, this matrix must be of size n x n.
		x : list
			First time series, which will be compared against time series y
		y : list 
			Second time series (reference)
		w : int
			Time warping window constraint (default = 0)
		g :	int
			ERP g-value (deafult = 0)

	Returns
	-------
		costMat : list
			A matrix (list of lists) describing the ERP cost matrix between the two time 
			series.  For a series of length n, this matrix will be of size n x n. 
	'''
	n = len(x)
	m = len(y)

	costMat = np.zeros((n,m))

	costMat[0,0] = dist[0,0]

	# Fill the edges
	for i in range(1, n):
		costMat[0,i] =  costMat[0,i-1] + abs(dist[0,i] - g)

	for i in range(1, n):
		costMat[i,0] = costMat[i-1,0] + abs(dist[i,0] - g)

	# Fill the rest of the matrix
	for i in range(1, n):
		for j in range(1, n):
			OpMatch = costMat[i-1,j-1] + dist[i,j]
			OpIns = costMat[i-1,j] + abs(x[i] - g)
			OpDel = costMat[i,j-1] + abs(y[i] - g)

			costMat[i,j] = min(OpMatch,OpDel,OpIns)

	# Apply warp window
	if w != 0:
		for i in range(0, n):
			for j in range(0, n):
				if abs(i-j) >= w:
					costMat[i,j] = np.inf

	return costMat


@jit
def DTWwarp(dist,x,y,w=0):
	'''Calcluates the ERP cost matrix between two time series.

	Parameters
	----------
		dist : list
			A matrix (list of lists) describing the L1-distance matrix between two 
			time series.  For a time series of length n, this matrix must be of size n x n.
		x : list
			First time series, which will be compared against time series y
		y : list 
			Second time series (reference)
		w : int
			Time warping window constraint (default = 0)

	Returns
	-------
		costMat : list
			A matrix (list of lists) describing the DTW cost matrix between the two time 
			series.  For a series of length n, this matrix will be of size n x n. 
	'''
	n = len(x)
	m = len(y)

	costMat = np.zeros((n,m))

	costMat[0,0] = dist[0,0]

	# Fill the edges
	for i in range(1, n):
		costMat[0,i] = dist[0,i] + costMat[0,i-1]

	for i in range(1, n):
		costMat[i,0] = dist[i,0] + costMat[i-1,0]

	# Fill the rest of the matrix
	for i in range(1, n):
		for j in range(1, n):
			minMove = min(costMat[i-1,j-1], costMat[i-1,j], costMat[i,j-1])
			costMat[i,j] = minMove + dist[i,j]

	# Apply warp window
	if w != 0:
		for i in range(0, n):
			for j in range(0, n):
				if abs(i-j) >= w:
					costMat[i,j] = np.inf

	return costMat

def backTrace(costMat,dist):
	'''Finds the optimal warping path by backtracking through the cost matrix.

	Parameters
	----------
		dist : list
			A matrix (list of lists) describing the L1-distance matrix between two 
			time series.  For a time series of length n, this matrix must be of size n x n.
		costMat : list
			A matrix (list of lists) describing the time-warped cost matrix between two 
			time series.  For a time series of length n, this matrix must be of size n x n.

	Returns
	-------
		path : list
			List of pairs of coordinates in time-space describing the backtrace through
			the cost matrix
		backTraceCost : float
			The sum cost of following the backtrace through the cost matrix
		warpStats : dict
			Warp statistics object, containing:		
		warpStats.timeAhead : int
			The number of periods that time series a was in sync with time series b.
		warpStats.timeAhead : int
			The number of periods that time series a was ahead of time series b.	
		warpStats.timeBehind : int
			The number of periods that time series a was behind of time series b.	
		warpStats.amountAhead : int
			The total sum of the number of periods that time series a was leading 
			time series b by.
		warpStats.amountBehind : int
			The total sum of the number of periods that time series a was lagging
			time series b by.
		warpStats.avgAhead : int
			Average amount of periods that a was ahead of a by, i.e. 
			amountAhead divided by timeAhead
		warpStats.avgAhead : int
			Average amount of periods that a was behind b by, i.e. 
			amountBehind divided by timeBehind
		warpStats.avgWarp : int
			Average amount of periods that a ahead or behind b by, i.e. 
			``(amountAhead - amountBehind) / (timeAhead + timeBehind + timeSync)``
			This will give positive values if a is on average ahead of b and negative
			values is a is on average behind b.
	'''
	
	timeAhead = 0
	timeBehind = 0
	timeSync = 0

	amountAhead = 0
	amountBehind = 0

	
	i = len(costMat) - 1
	j = len(costMat[0]) - 1
	path = np.array([i,j])

	backTraceCost = dist[i,j]

	while i>0 or j>0:
		if i==0:
			# Edge condition (only one direction)
			j = j - 1
		elif j==0:
			# Edge condition (only one direction)
			i = i - 1
		else:
			minMove = min(costMat[i-1,j-1], costMat[i-1,j], costMat[i,j-1])
			if costMat[i-1,j] == minMove:
				i = i - 1
			elif costMat[i,j-1] == minMove:
				j = j - 1
			else:
				i = i - 1
				j = j - 1
		
		backTraceCost += dist[i,j]
		path = np.vstack([path,[i,j]])

		if j > i:
			timeAhead += 1
			amountAhead += j - i
		elif i > j:
			timeBehind += 1
			amountBehind += i - j
		else:
			timeSync +=1

	warpStats = {}
	warpStats["timeAhead"] = timeAhead
	warpStats["timeBehind"] = timeBehind
	warpStats["timeSync"] = timeSync
	warpStats["amountAhead"] = amountAhead
	warpStats["amountBehind"] = amountBehind
	warpStats["avgAhead"] = 0
	warpStats["avgBehind"] = 0

	if timeAhead > 0:
		warpStats["avgAhead"] = amountAhead / timeAhead

	if timeBehind > 0:
		warpStats["avgBehind"] = amountBehind / timeBehind

	warpStats["avgWarp"] = (amountBehind - amountAhead) / (timeAhead + timeBehind + timeSync)

	return path, backTraceCost, warpStats

