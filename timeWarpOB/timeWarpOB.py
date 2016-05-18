def timeWarp(a,b,method='DTW',window=0,retMat=True,**kwargs):
	'''Time warping interface

	A - timeseries 1 as a python list
	B - timeseries 2 as a python list
	method - DTW, ERP
	window = 0 for no window
	retMat - return cost and distance matrices
	kwargs 
		- ERPg - ERP g value
	'''

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
	cost = costMat[cIndex][cIndex]

	# Backtrace the warp path
	path, backTraceCost, warpStats = backTrace(costMat,dist)

	# Return the results
	if retMat == True:
		warpObj["costMat"] = costMat
		warpObj["distMat"] = dist
	
	warpObj["cost"] = cost
	warpObj["backTraceCost"] = backTraceCost
	warpObj["warpStats"] = warpStats
	warpObj["backTracePath"] = path
	
	if window == 0:
		warpObj["warpWindow"] = len(a)
	else:
		warpObj["warpWindow"] = window

	return warpObj



def L1distances(a,b):
	'''Calcluates the L1 distance matrix between two time series.
	'''
	n = len(a)
	m = len(b)

	distance = [[] for _ in range(n)]
	for i in range(0, n):
		for j in range(0, m):
			distance[i].append(0)

	for i in range(n):
		for j in range(m):
			if a[i] == 'nan' or b[j] == 'nan':
				distance[i][j] = 0
			else:
				distance[i][j] = abs(a[i] - b[j])

	return distance 


def ERPwarp(dist,x,y,w=0,g=0):
	'''Calcluates the ERP cost matrix between two time series.
	'''
	n = len(x)
	m = len(y)

	costMat = [[] for _ in range(n)]
	for i in range(0, n):
		for j in range(0, m):
			costMat[i].append(0)

	costMat[0][0] = dist[0][0]

	# Apply warp window
	if w != 0:
		for i in range(0, n):
			for j in range(0, n):
				if abs(i-j) >= w:
					costMat[i][j] = float("inf")

	# Fill the edges
	for i in range(1, n):
		costMat[0][i] =  costMat[0][i-1] + abs(dist[0][i] - g)

	for i in range(1, n):
		costMat[i][0] = costMat[i-1][0] + abs(dist[i][0] - g)

	# Fill the rest of the matrix
	for i in range(1, n):
		for j in range(1, n):
			OpMatch = costMat[i-1][j-1] + dist[i][j]
			OpIns = costMat[i-1][j] + abs(x[i] - g)
			OpDel = costMat[i][j-1] + abs(y[i] - g)

			costMat[i][j] = min(OpMatch,OpDel,OpIns)

	return costMat



def DTWwarp(dist,x,y,w=0):
	'''Calcluates the ERP cost matrix between two time series.
	'''
	n = len(x)
	m = len(y)

	costMat = [[] for _ in range(n)]
	for i in range(0, n):
		for j in range(0, m):
			costMat[i].append(0)

	costMat[0][0] = dist[0][0]

	# Fill the edges
	for i in range(1, n):
		costMat[0][i] = dist[0][i] + costMat[0][i-1]

	for i in range(1, n):
		costMat[i][0] = dist[i][0] + costMat[i-1][0]

	# Fill the rest of the matrix
	for i in range(1, n):
		for j in range(1, n):
			minMove = min(costMat[i-1][j-1], costMat[i-1][j], costMat[i][j-1])
			costMat[i][j] = minMove + dist[i][j]

	# Apply warp window
	if w != 0:
		for i in range(0, n):
			for j in range(0, n):
				if abs(i-j) >= w:
					costMat[i][j] = float("inf")

	return costMat


def backTrace(costMat,dist):
	'''Finds the optimal warping path by backtracking
	'''
	
	timeAhead = 0
	timeBehind = 0
	timeSync = 0

	amountAhead = 0
	amountBehind = 0

	path = []
	i = len(costMat) - 1
	j = len(costMat[0]) - 1

	path.append([i,j])
	backTraceCost = dist[i][j]

	while i>0 or j>0:
		if i==0:
			# Edge condition (only one direction)
			j = j - 1
		elif j==0:
			# Edge condition (only one direction)
			i = i - 1
		else:
			minMove = min(costMat[i-1][j-1], costMat[i-1][j], costMat[i][j-1])
			if costMat[i-1][j] == minMove:
				i = i - 1
			elif costMat[i][j-1] == minMove:
				j = j - 1
			else:
				i = i - 1
				j = j - 1
		
		backTraceCost += dist[i][j]
		path.append([i,j])

		if i > j:
			timeAhead += 1
			amountAhead += i - j
		elif j > i:
			timeBehind += 1
			amountBehind += j - i
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

	warpStats["avgWarp"] = (amountAhead - amountBehind) / (timeAhead + timeBehind + timeSync)

	return path, backTraceCost, warpStats

