NAME
	cpd4sits.py -- changepoint detection for satellite image time series (SITS)

SYNOPSIS
	python	cpd4sits.py	[-c cost] [-e day_end] [-g gap] [-m min_size] [-p penalty] [-s day_start]
						[-w window] directory features

DESCRIPTION

	The script reads the CSV files of the specified features, separated by a dash (ex. VH-NDVI),
	in the target directory (ex. AAA). If the change detection is performed (no errors and/or
	sufficient number of data points), two additional CSV files are generated (‘AAA_dates.csv’, 
	‘AAA_features.csv’).
	‘AAA_dates.csv’ contains the estimated change dates in the specified time period (empty if no
	change has been detected). 
	‘AAA_features.csv’ contains the features used to perform the change detection.

     
	The following options are available:

	-h				Display usage

	-c cost			Cost function. Two possible values: ‘l1’ (least absolute deviation) or ‘l2’
					(least squares deviation). 
					Default is ‘l2’.

	-e day_end		Last day of analysis. Format: YYYY-MM-DD. 
					Default is day of execution.

	-g gap			Maximum allowed gap between dates in the time series.
					Default is 120 (days).

	-m min_size		Minimum distance between change points.
					Default is 30 (days).

	-p penalty		Penalty term to control the number of change points.
					Default is log(n), where n is the length of the time series.

	-s day_start	First day of analysis. Format: YYYY-MM-DD. 
					Default is day_end-4Y.

	-w window		Smoothing window (standard deviation of the Gaussian kernel).
					Default is 61.


EXAMPLES

	1.	Analyze all the VV Sentinel-1 temporal profiles and the Sentinel-2 NDVI temporal profile
		using the default parameters:

			$ python cpd4sits.py /path/to/files VV-NDVI

     
	2.	Analyze the VH_37 Sentinel-1 temporal profile, the Sentinel-2 NDVI and SBI temporal profiles
		from 2018 to 2021 using the L1 cost function:

			$ python cpd4sits.py –s 2018-01-01 –e 2021-12-31 –c l1 /path/to/files VH_37-NDVI-SBI



DOCKER

	-	Build the docker image:

			$ docker build -t cpd4sits /path/to/CPD4SITS

	-	To analyze folder ‘path/to/folder/AAA’ (as in Example 1), run:

			$ docker run --rm -v /path/to/folder:/usr/src/app/data cpd4sits data/AAA VV-NDVI
