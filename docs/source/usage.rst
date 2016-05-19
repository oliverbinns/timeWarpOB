User guide
==========

Background to Time Warping
--------------------------

Time warping is used to determine the similarity between two time series that vary in speed along the time axis.  By warping the time axis on one of the series, it is possible to make the time series 'match' each other, with the amount of warping being a measure of the dis-similarity of the series.  By dynamically changing the amount of warping along the time-axis, it is possible to deal with time series that accelerate or decelerate at different points in the series.  Because of this, time warping has applications in many areas, including speech recognition, video analysis and understanding of market data.  The output from time warping can be used as a similarity distance metric that is fed into other machine learning methods such as clustering.

Time warping techniques are based on edit distance in strings, which calculates the 'cost' of converting one string into another by making a series of insertion, deletion or replacement operations.  The optimal (lowest) number of these operations can be determined using a dynamic programming algorithm [#fdynProg]_. The same methods can be used, but replacing the symbols in the two strings with the numeric values of a time series. 

*timeWarpOB* implements two methods of warping the time axis, namely Dynamic Time Warping (DTW) and Edit distance with Real Penalty (ERP) [#fERP]_.  

Both work by taking two time series of length :math:`n` and initially forming a :math:`n \times n` matrix measuring the pairwise Euclidean distance between every point on the two time series (the distance matrix).  Both algorithms will then create a second :math:`n \times n` that describes the cumulative minimum 'cost' of moving through the distance matrix (the cost matrix).  Depending on the method, the costs involved are calculated differently.  After this cost matrix has been produced, a back tracing routine works backwards through the matrix and finds the lowest cost route.  This path describes the warping of the time series with respect to each other (i.e. where one is accelerating or decelerating relative to the other)

In DTW, the algorithm will traverse the distance matrix and calculate the cumulative distance, by the minimum of moving one step in both time series (i.e. when they are in sync) or moving only one step in one of the time series (i.e. when one is accelerating relative to another.  In ERP, the cumulative distance is based upon a penalty factor (:math:`g`) when moving along only one of the time series.  For a formal definition of these cost functions, see [#fERP]_

In order to prevent the back tracing function from selecting a circuitous route through the cost matrix and warping large parts of a time series in a way that is not realistic for the physical application, it is possible to apply a 'warp window' to the cost matrix, which sets all values a given distance from the diagonal to a very high number (or infinity), so the back trace algorithm does not go through them.

For a comparison of various time warping techniques, including some not implemented by *timeWarpOB*, see this paper: [#fCompare]_.  Additionally this paper [#fMJC]_ details the Minimum Jump cost (MJC) method.

NB: with very long time series, the methods used in this package may be slow.  This is as for a time series of length :math:`n`, an :math:`n \times n` matrix of values must be populated, meaning the algorithm runs on :math:`\mathcal{O}(n^2)`.  Alternatives for large time series include the FTSE method [#fFTSE]_ (not implemented in *timeWarpOB*).


Example usage
-------------

**NOTE:** This section assumes you have followed the instructions in the :doc:`installation` section.

First, import timeWarpOB::

	import timeWarpOB as tw

Then prepare two python lists of data, along with an optional list containing timestamps  If you have data loaded into a pandas dataframe called ``df``, with two columns and an index of timestamps, you can convert them by::
	
	a = list(df["columnA"])
	b = list(df["columnB"])
	ts = list(df.index)

Alternatively, generate a sin and cos series using the built-in test function (passing ``n`` for the number of half-cycles to generate)::

	x, y, ts = tw.tests.basic.sinCos(n=2)

The two timeseries then be warped using the ``timeWarp()`` function, to return a ``warpObject``::
	
	wo = tw.timeWarp(a,b)

This will return a warp object.  Useful statistics about the time warping result can be found in ``wo['warpStats']`` and the total warp cost can be found in ``wo['backTraceCost']``.  More information about the warp object and the calculation of the statistics can be found in the :doc:`APIref` section.

To plot the results of the time warp, use::

	tw.plotting.plotWarp(x,y,wo,ts)

Which will give a warping result as a matplotlib chart, containing the following items:

	* The central chart displays the cost matrix as a series of grey pixels in a graph.  The darker pixels represent higher costs.  Time series 'a' runs along the vertical axis from bottom to top and time series 'b' runs along the horizontal axis from left to right .  The diagonal line (yellow) represents the path that would be taken if the two series were perfectly in sync.  The diagonal, dashed magenta lines show the extent of the warp window (if applied) and the red line shows the back-traced path through the cost matrix.  When the red line deviates from the yellow diagonal line, the time series are accelerating or decelerating with respect to each other.  If the red line moves closer to the top-left corner, then this indicates that time series a is moving ahead of time series b (and *vice versa*).  
	* To the left of the central plot is a graph of time series a (rotated, so each point aligns with its position on the central chart).  Below the central plot is a graph of time series b.
	* To the right of the central plot, if a graph which shows the back-traced path, but rotated by 45 degrees to facilitate better understanding of where the time series accelerate or decelerate relative to one another.  A dashed cyan line is added to show the average position of the red line (which is equal to the ``warpStats.avgWarp`` value)
	* Above the central plot, both time series are plotted against each other and red lines are added to show how point on each time series are related according to the back-traced warp path.


References
----------
.. [#fdynProg] `Wagner-Fischer algorithm (Wikipedia) <https://en.wikipedia.org/wiki/Wagner--Fischer_algorithm>`_

.. [#fERP] Chen, Lei, and Raymond T Ng. 2004. "On the Marriage of Lp-Norms and Edit Distance.." Vldb, 792--803.

.. [#fCompare] Serrà, Joan, and Josep Lluís Arcos. 2014. "An Empirical Evaluation of Similarity Measures for Time Series Classification.." Knowl.-Based Syst. () cs.LG: 305--14. doi:10.1016/j.knosys.2014.04.035.

.. [#fMJC] Serrà, Joan, and Josep Lluís Arcos. 2012. "A Competitive Measure to Assess the Similarity Between Two Time Series." In Case-Based Reasoning Research and Development, edited by Belén Díaz Agudo and Ian Watson, 7466:414--27. Lecture Notes in Computer Science. Berlin, Heidelberg: Springer Berlin Heidelberg. doi:10.1007/978-3-642-32986-9_31.

.. [#fFTSE] Morse, Michael D, and Jignesh M Patel. 2007. "An Efficient and Accurate Method for Evaluating Time Series Similarity.." Sigmod. New York, New York, USA: ACM Press, 569--80. doi:10.1145/1247480.1247544.

