# Brief explanation of some files in this directory

First, a story. I ran [this](../src/backtests/find_optimal_dynema.cpp) on a few different datasets 
to determine what the best parameters for my so-called dynamic EMA strategy. 
The results of one dataset conflicted with those of the other. To determine which of these should be 
used in live trading I decided I would simulate the strategy using the optimal parameters for  
each dataset on the other dataset. I decided to use the best five parameters for each ticker. 
The aforementioned simulation runs the dynamic EMA strategy on increasingly longer periods of time  
starting with a year. The following is a collection of scripts to automate doing just that. 

**NOTE: Some of the file paths in these scripts are probably incorrect if run from this directory**

* `convolute1.sh` runs the simulation on the various time periods using data from 
[this](../data/datset1/) dataset 

* `convolute2.sh` does the same as the above, but with data from [this](../data/dataset2/) dataset. 

* `cross_params.py` generates shell commands for running `convolute1.sh` and
`convolute2.sh` with the right arguments; the arguments being the ticker and the different sets of "optimal"
 parameters 

* `count.py` counts how many times the algorithm beat the market when given output from running the
commands that `cross_params.py` generates. Ultimately, it summarizes the results of testing
the dynamic EMA parameters "against each other".

* `misc.py` currently just has code that generates links to get historical data from yahoo finance. Yes, 
`misc.py` isn't a great name but it's literally for miscellaneous scripts that I may or may not use again. 

