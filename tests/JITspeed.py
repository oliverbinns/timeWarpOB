from numba import jit
import numpy as np
import cProfile
import timeit

def L1distances(a,b):
	n = len(a)
	m = len(b)

	distance = [[] for _ in range(n)]
	for i in range(0, n):
		for j in range(0, m):
			distance[i].append(0)

	containsNaN = False
	for i in range(n):
		if a[i] == 'nan' or b[j] == 'nan':
			containsNaN = True

	if(containsNaN):
		print("Warning: at least one of the time series contains NaN values.  Time Warping performance will be impacted.")
		for i in range(n):
			for j in range(m):
				if a[i] == 'nan' or b[j] == 'nan':
					distance[i][j] = 0
				else:
					distance[i][j] = abs(a[i] - b[j])
	else:
		for i in range(n):
			for j in range(m):
				distance[i][j] = abs(a[i] - b[j])

	return distance 


def L1distancesNumpy(a,b):
	n = len(a)
	m = len(b)

	distance = np.zeros((n,m))

	for i in range(n):
		for j in range(m):
			distance[i,j] = abs(a[i] - b[j])

	return distance 

@jit
def L1distancesNumpyFast(a,b):
	n = len(a)
	m = len(b)

	distance = np.zeros((n,m))

	for i in range(n):
		for j in range(m):
			distance[i,j] = abs(a[i] - b[j])

	return distance 


@jit
def L1distancesFast(a,b):
	n = len(a)
	m = len(b)

	distance = [0.0]
	for i in range(1, n):
		r = [0.0]
		for j in range(1, m):
			r.append(0.0)
		
		distance.append(r)


	for i in range(n):
		for j in range(m):
			distance[i][j] = abs(a[i] - b[j])

	return distance 


n = 2
l = 1000
ts = list(np.linspace(0, n*np.pi, l))
x = list(np.sin(ts))
y = list(np.cos(ts))

npX = np.array(x)
npY = np.array(y)

cProfile.run("L1distances(x,y)",sort="tottime")
#cProfile.run("L1distancesFast(x,y)",sort="tottime")
cProfile.run("L1distancesNumpy(npX,npY)",sort="tottime")
cProfile.run("L1distancesNumpyFast(npX,npY)",sort="tottime")


def test1():
	a = L1distances(x,y)
	return 0

def test2():
	a = L1distancesNumpy(npX,npY)
	return 0

def test3():
	a = L1distancesNumpyFast(npX,npY)
	return 0

timeit.timeit(test1)
timeit.timeit(test2)
timeit.timeit(test3)