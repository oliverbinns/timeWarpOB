Installation
============

timeWarpOB can be installed by using pip::

	pip install timeWarpOB

Note that timeWarpOB requires numpy to be be installed for handling the time series and results arrays.  The matplotplib module is also required for plotting the warp graphs.

Calculation speed can be substantially improved by installing the numba module, which compiles some of the inner calculation loops to give calculation performance comparable to native compiled code. However, timeWarpOB can still run without numba.  To check if numba is detected by timeWarpOB, run the following in python::

	import timeWarpOB as tw
	print(tw.foundNumba)

You can quickly test the tiemWarpOB installation by using::

	x, y, ts = tw.tests.basic.sinCos()
	tw.tests.basic.testWarp(x,y,ts)

This will generate two time series based on a sin and cos function and attempt to warp them.  The warp statistics will be printed to the console and a plot showing the warp result will be shown.