 
# Jean-paul Ventura
# January 12, 2017
# Modified: February 20th, 2016

from astropy.io import fits
import numpy as np


# Calculate equivalent width
def eqwidth(filename,wavelength1,wavelength2,wavelength3,wavelength4):
	'''

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
	
	The measured equivalent width of the spectral emission/absorption feature

	'''

	# Open .fits file 
	hdu = fits.open(filename) 

	# Define wavelength and flux arrays by accessing .fits sloan data
	lmbda = 10**np.array(hdu[1].data['loglam'])
	flux = hdu[1].data['flux']


	# Normalize flux by dividing flux array by mean flux value over relatively quiet
	# continuum region
	indx = np.where((lmbda > 8250) & (lmbda < 8350))
	avgval = flux[indx].mean()
	nflux = flux/avgval


	# Index for continuum region where line feature is found
	fuindx = (lmbda >= wavelength1) & (lmbda <= wavelength4)
	
	# Index for the line feature itself
	coindx = ((lmbda >= wavelength1) & (lmbda <= wavelength2)) | ((lmbda >= wavelength3) & (lmbda <= wavelength4))

	# Isolate the line feature wavelength region
	x1 = lmbda[coindx]
	
	#Isolate the normalized flux over the line feature wavelength region
	y1 = nflux[coindx]
	
	#fit 1st degree polynomial to the line feature
	m,c = np.polyfit(x1,y1,1)
	
	#print m,c
	#rms = sqrt( mean( (m*x1 + c - y1)**2 ) )
	
	lmbda = lmbda[fuindx]
	flux = nflux[fuindx]
	
	
	dlmbda= lmbda[2]-lmbda[1]
	fitl = m*lmbda + c

	

	ewindx = np.where((lmbda >= wavelength2) & (lmbda <= wavelength3))
	eqwi = sum(1-nflux[ewindx])*dlmbda

	# For error
	#fx1, err = mcerr(wav,dat,w2,w3,m,c,rms)

	return eqwi


#Calculate line height of spectral emission feature
def line_height(filename,wavelength1,wavelength2,wavelength3,wavelength4):
	
	# Open sloan .fits file
	hdu = fits.open(filename) 

	#Construct wavelength (lmbda) and flux arrays from data
	lmbda = 10**np.array(hdu[1].data['loglam'])
	flux = hdu[1].data['flux']

	# Normalize flux by dividing flux array by mean flux value over relatively quiet
	# continuum region
	indx = np.where((lmbda > 8250) & (lmbda < 8350))
	avgval = flux[indx].mean()
	nflux = flux/avgval

	# designate fundamental and continuum indices
	fuind = (lmbda >= wavelength1) & (lmbda <= wavelength4)
	coind = ((lmbda >= wavelength1) & (lmbda <= wavelength2)) | ((lmbda >= wavelength3) & (lmbda <= wavelength4))

	lmbda = lmbda[fuind]
	flux = nflux[fuind]
	x1 = lmbda[coind]
	y1 = nflux[coind]
	m,c = np.polyfit(x1,y1,1)
	#print m,c
	rms = sqrt( mean( (m*x1 + c - y1)**2 ) )
	

	lnheight = max(y1)-min(y1)

	return lnheight


