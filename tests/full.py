import numpy as np
import timeWarpOB as tw
import unittest

class test_full(unittest.TestCase):
	'''
	Unit testing suite for TimeWarpOB.  To run, use python full.py 
	at a Command Prompt.
	'''

	def testSinCos(self):
		'''Runs multiple sin/cos and check the warp is equal to pi/2'''
		def testSinCos(n,l):
			ts = list(np.linspace(0, n*np.pi, l))
			x = list(np.sin(ts))
			y = list(np.cos(ts))

			wo = tw.timeWarp(x,y,method='DTW')

			avgWarp = wo["warpStats"]["avgBehind"]

			avgWarpAng = ( (n*np.pi) / l) * avgWarp

			return (np.pi / 2) - avgWarpAng

		for i in range(2,500):
			d = testSinCos(i,(2*i))
			self.assertTrue( (round(d * 1000000)/1000000) == 0)


	def testWindow(self):
		'''Checks the warp window works by setting it equal to 1 
		(0 warp deviation should be reported)'''

		ts = list(np.linspace(0, 4*np.pi, 1000))
		x = list(np.sin(ts))
		y = list(np.cos(ts))

		wo = tw.timeWarp(x,y,method='DTW', window=1)
		self.assertTrue(wo["warpStats"]["avgWarp"] == 0)

	def testL1Flat(self):
		'''Check that the L1 distance is calcuated properly, 
		using two "flat" series'''

		for i in range(1,500):
			for j in range(0,100,20):
				x = list(np.ones(i) * j)
				y = list(np.ones(i))
				c = tw.L1distances(x,y)

				expected = abs(((i*i*1)-(i*i*j)))

				self.assertTrue(abs(c.sum()) == expected)



	def testL1Slope(self):
		'''Check that the L1 distance is calcuated properly, 
		using two linearly sloping series'''

		x = []
		y = []
		l = 500

		for i in range(1,l+1):
			x.append(i)
			y.append(i)

		c = tw.L1distances(x,y)

		self.assertTrue(c[0].sum() == l*(0+(l-1))/2)

		for i in range(1,l):
			self.assertTrue(c[i][i] == 0)


	def testCostMat(self):
		''' Test cost matrix calcualtion for DTW and ERP with 
		linearly sloping time series'''

		x = []
		y = []
		l = 500

		for i in range(1,l+1):
			x.append(i)
			y.append(i)

		c = tw.L1distances(x,y)

		self.assertTrue(c[0].sum() == l*(0+(l-1))/2)
		d = tw.timeWarpOB.DTWwarp(c,x,y,w=0)
		e = tw.timeWarpOB.ERPwarp(c,x,y,w=500,g=0)


		for i in range(0,l):
			r1 = 1/(c[i].sum() / d[i].sum())
			r2 = 1/(c[l-i-1].sum() / d[l-i-1].sum())
			self.assertTrue(r1 == r2)

			self.assertTrue(d[i][i] == 0)
			self.assertTrue(e[i][i] == 0)


if __name__ == '__main__':
    unittest.main()




