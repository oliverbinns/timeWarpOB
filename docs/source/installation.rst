Installation
============

timeWarpOB can be installed by using pip::

	pip install timeWarpOB

Note that timeWarpOB requires matplotplib for plotting the warp graphs and numpy for the test cases.

You can quickly test the installation by using::

	x, y, ts = tw.tests.basic.sinCos()
	tw.tests.basic.testWarp(x,y,ts)

This will generate two time series based on a sin and cos function and attempt to warp them.  The warp statistics will be printed to the console and a plot showing the warp result will be shown.