 
# Jean-paul Ventura
# January 12, 2017
# Modified: February 20th, 2016

from astropy.io import fits
import numpy as np


def eqwidth(filename,wavelength1,wavelength2,wavelength3,wavelength4):
	"""

	This function measures the equivalent width of spectral emission/absorption features.
	
	====================
	Function parameters: 
	====================
	
	filename 	- SDSS spectra .fits filename entered as a string. You may specify entire
				  path as a string, or if file is located in the current working directory, 
				  simply the filename (e.g. 'SDSS-12345.fits') 
	
	wavelength1 - wavelength value where continuum region to the left of the spectral feature begins.
	
	wavelength2 - wavelength value where continuum region to the left of the spectral feature ends.
	
	wavelength3 - wavelength value where continuum region to the right of the spectral feature begins.
	
	wavelength4 - wavelength value where continuum region to the right of the spectral feature ends.
	
	=================
	Function returns:
	=================
	
	 eqwi - The measured equivalent width of the spectral emission/absorption feature

	"""

	# Open .fits file 
	hdu = fits.open(filename) 

	# Define wavelength and flux arrays by accessing .fits sloan data
	lmbda = 10**np.array(hdu[1].data['loglam'])
	flux = hdu[1].data['flux']



	# Index for continuum region where entire line feature is found (wings + emission line)
	fuindx = (lmbda >= wavelength1) & (lmbda <= wavelength4)
	
	# Index for both of the wings of the line feature
	coindx = ((lmbda >= wavelength1) & (lmbda <= wavelength2)) | ((lmbda >= wavelength3) & (lmbda <= wavelength4))

	# Isolate the wavelength subarrays pertaining to both of the wings of the line feature
	x1 = lmbda[coindx]
	
	#Isolate the normalized flux subarrays of the line features wings.
	y1 = nflux[coindx]
	
	# Generate first degree polynomial coefficients that correspond to the line wings
	m,c = np.polyfit(x1,y1,1)
	#print m,c
	
	# calculate the RMSE for the baseline for later use to generate error array.
	rmse = sqrt( mean( (m*x1 + c - y1)**2 ) )
	
	# Assign the wavelength and normalized flux arrays over the entire feature (wings + line) to new variables
	lmbda = lmbda[fuindx]
	flux = flux[fuindx]
	

	# using the coefficients of the deg(1) polynomial generated earlier from the wings, fit a line to them
	# in order to establish the baseline for the line feature.
	fitl = np.array(m*lmbda + c)
	
	# Normalize the flux array by dividing it by the fitline.
	nflux = flux/fitline

	# assign the differential wavelength element to a variable.
	dlmbda= lmbda[2]-lmbda[1]
	
	# Create index for the wavelength of the line feature itself (line without the wings)
	ewindx = np.where((lmbda >= wavelength2) & (lmbda <= wavelength3))
	
	# Sum continuosly over the normalized flux array and assign result to a variable.
	eqwi = sum(1-nflux[ewindx])*dlmbda
 	
 	# Calculate the uncertainty in the equivalent with measurement
	eqwi1, err = mcerror(lmbda,flux,wavelength2,wavelength3,m,c,rmse)

	# Return the result of the equivalent width measurement and associated error
	return eqwi, err


def mcerror(lmbda,flux,wavelength2,wavelength3,m,c,rmse):
	"""
	This function calculates the error of an equivalent width measurement. The error is characterized
	by the value of the RMSE above or below the baseline generated for the feature. The error is calculated
	via the mean of multiple error values generated via 3000 iterations of the monte carlo method for the 
	single emission feature.

	==========
	ARGUMENTS:
	==========

	lmbda -  Wavelength array of entire feature (wings + line).

	flux  -  Normalized flux array of the entire feature (wings + line)

	wavelength2 - wavelength value where continuum region to the left of the spectral feature ends.
	
	wavelength3 - wavelength value where continuum region to the right of the spectral feature begins.

	m,c   -  Coefficients of a first degree polynomial fit to the wings of the entire line feature.

	rmse  -  RMSE error calculated over the first degree polynomial line fit to the wings(baseline). 

	========
	RETURNS:
	========
	
 	error and standard deviation of the equivalent width measurement taken over 3000 monte carlo iterations

	"""
	# assign the number of monte carlo iterations to variable 'size'.
	size =  3000
	
	# Create an empty list to which eqmeasurements will be appended.
	guess= []
	
	# Define the differential wavelength element and assign to variable 'dlmbda'.
	dlmbda = lmbda[2]-lmbda[1]

	# Iterate error calculations over equivalent width measurement 3000 times by drawing randomly from 
	# a uniform distribution about the RMSE. Then take the mean and std dev of those values and return values.
	for i in range(size):
	  fitl = m*lmbda + c + np.random.uniform(-1,1)*rmse
	  nflux = flux / fitl
	  ewindx = (lmbda >= wavelength2) & (lmbda <= wavelength3)
	  fx = sum(1-nflux[ewindx]) *dlmbda
	  guess.append(fx)

	return np.mean(guess),np.std(guess)


#Calculate line height of spectral emission feature
def line_height(filename,wavelength1,wavelength2,wavelength3,wavelength4):
	"""
	Tnis function calculates the emission line feature height as the vertical-distance between the 
	maximum flux value and minimum flux value over the feature interval.

	==========
	ARGUMENTS:
	==========
	
	filename 	- SDSS spectra .fits filename entered as a string. You may specify entire
				  path as a string, or if file is located in the current working directory, 
				  simply the filename (e.g. 'SDSS-12345.fits') 
	
	wavelength1 - wavelength value where continuum region to the left of the spectral feature begins.
	
	wavelength2 - wavelength value where continuum region to the left of the spectral feature ends.
	
	wavelength3 - wavelength value where continuum region to the right of the spectral feature begins.
	
	wavelength4 - wavelength value where continuum region to the right of the spectral feature ends.

	========
	RETURNS:
	========

	lnheight - line height of spectral emission feature.

	"""
	
	# Open sloan .fits file
	hdu = fits.open(filename) 

	#Construct wavelength (lmbda) and flux arrays from data
	lmbda = 10**np.array(hdu[1].data['loglam'])
	flux = hdu[1].data['flux']

 	# Index for continuum region where entire line feature is found (wings + emission line)
	fuindx = (lmbda >= wavelength1) & (lmbda <= wavelength4)
	
	# Index for both of the wings of the line feature
	coindx = ((lmbda >= wavelength1) & (lmbda <= wavelength2)) | ((lmbda >= wavelength3) & (lmbda <= wavelength4))

	# Isolate the wavelength subarrays pertaining to both of the wings of the line feature
	x1 = lmbda[coindx]
	
	#Isolate the normalized flux subarrays of the line features wings.
	y1 = nflux[coindx]
	
	# Generate first degree polynomial coefficients that correspond to the line wings
	m,c = np.polyfit(x1,y1,1)
	#print m,c
	
	# calculate the RMSE for the baseline for later use to generate error array.
	rmse = sqrt( mean( (m*x1 + c - y1)**2 ) )
	
	# Assign the wavelength and normalized flux arrays over the entire feature (wings + line) to new variables
	lmbda = lmbda[fuindx]
	flux = flux[fuindx]
	
	# using the coefficients of the deg(1) polynomial generated earlier from the wings, fit a line to them
	# in order to establish the baseline for the line feature.
	fitl = np.array(m*lmbda + c)
	
	# Normalize the flux array by dividing it by the fitline.
	nflux = np.array(flux/fitline)

	# Create index for the wavelength of the line feature itself (line without the wings)
	ewindx = np.where((lmbda >= wavelength2) & (lmbda <= wavelength3))

	# Calculate the line height for the featrue and assign to a variable.
	lnheight = max(nflux[ewindx])-min(nflux[ewindx])
	
	return lnheight


