
# Jean-paul Ventura
# January 12, 2017
# Modified: February 20th, 2016

from astropy.io import fits
import numpy as np

# Calculate equivalent width
def eqwidth(filename,wavelength1,wavelength2,wavelength3,wavelength4):
"""
This function measures the equivalent width of spectral emission/absorption features.

==========
Arguments: 
==========

filename 	- SDSS spectra .fits filename entered as a string. You may specify entire
			  path as a string, or if file is located in the current working directory, 
			  simply the filename (e.g. 'SDSS-12345.fits') 

wavelength1 - wavelength value where continuum region to the left of the spectral feature begins.

wavelength2 - wavelength value where continuum region to the left of the spectral feature ends.

wavelength3 - wavelength value where continuum region to the right of the spectral feature begins.

wavelength4 - wavelength value where continuum region to the right of the spectral feature ends.

========
Returns:
========

The measured equivalent width of the spectral emission/absorption feature
"""
	
	hdu = fits.open(filename) 

	lambda = 10**np.array(hdu[1].data['loglam'])
	flux = hdu[1].data['flux']

	#designate fundamental and continuum indices
	fuind = (lambda >= wavelength1) & (lambda <= wavelength4)
	coind = ((lambda >= wavelength1) & (lambda <= wavelength2)) | ((lambda >= wavelength3) & (lambda <= wavelength4))

	x1 = lambda[coind]
	y1 = flux[coind]
	m,c = np.polyfit(x1,y1,1)
	# #print m,c
	# rms = sqrt( mean( (m*x1 + c - y1)**2 ) )
	indx = np.where((lambda > 8250) & (lambda < 8350))
	avgval = flux[indx].mean()
	nflux = flux/avgval
	lambda = lambda[fuind]
	flux = flux[fuind]
	
	
	dlambda= lambda[2]-lambda[1]
	fitl = m*lambda + c

	

	ewind = np.where((lambda >= w2) & (lambda <= w3))
	eqwi = sum(1-nflux[ewind])*dlambda

	# For error
	#fx1, err = mcerr(lambda,nflux,wavelenth2,wavelength3,m,c,rms)

	return eqwi



def mcerr(lambda,flux,wavelength1,wavelength2,m,c,rms):
	size = 3000
	guess = []
	dlam = lambda[2]-lambda[1]

	for i in range(size):
	  fitl = m*lambda + c + uniform(-1,1)*rms
	  ndat = dat / fitl
	  ewindx = (wav >= w1) & (wav <= w2)
	  fx = sum(1-ndat[ewindx]) *dlam
	  guess.append(fx)

	return mean(guess),std(guess)

# =========================




# #hdu.close()
# 
# # Halpha
# w1 = 6548
# w2 = 6556.
# w3 = 6570
# w4 = 6580
# st = 2 # spread to consider
# cc = 0.002

 # value = eqwidth(wave,data,w1,w2,w3,w4)
# print value
# val1, err1 = mcew(wave,data,w1,w2,w3,w4,st,cc)
# val1 = ewidth(wave,data,w1,w2,w3,w4)
# print val1

 # 
# fuind = (wave >= w1) & (wave <= w4)
# coind = ((wave >= w1) & (wave <= w2)) | ((wave >= w3) & (wave <= w4))
# 
# x1 = wave[coind]
# y1 = data[coind]
# m,c = polyfit(x1,y1,1)
# 
# wav1 = wave[fuind]
# dat1 = data[fuind]
# fitl1 = m*wav1 + c
# ndat1 = dat1 / fitl1
# 
# 
# fuind = (wave >= 6540) & (wave <= 6750)
# data = data[fuind]
# wave = wave[fuind]
# 
# plot(wave,data,"k")
# plot(wav1,dat1,"b")
# plot(wav1,fitl1,"r")
# 
# axvspan(w2,w3,facecolor="0.8")

 
 
#  Li
# w1 = 6700.5
# w2 = 6706.
# w3 = 6711.5
# w4 = 6713.
# st = 1.
# cc = 0.000
# 
# #val2, err2 = mcew(wave,data,w1,w2,w3,w4,st,cc)
# val2, err2 = ewidth(wave,data,w1,w2,w3,w4)
# print val2, err2
# 
# 
# fuind = (wave >= w1) & (wave <= w4)
# coind = ((wave >= w1) & (wave <= w2)) | ((wave >= w3) & (wave <= w4))
# 
# x1 = wave[coind]
# y1 = data[coind]
# m,c = polyfit(x1,y1,1)
# 
# wav2 = wave[fuind]
# dat2 = data[fuind]
# fitl2 = m*wav2 + c
# ndat2 = dat2 / fitl2
# 
# 
# plot(wav2,dat2,"b")
# plot(wav2,fitl2,"r")
# axvspan(w2,w3,facecolor="0.8")
# 
# tout = '%s: %2.3f+/-%0.3f, %1.3f+/-%0.3f' % (name[0], val1, err1, val2, err2) 
# 
# xlabel('Wavelength (Ang)')
# ylabel('Flux')
# title(tout)
# ranges = axis()
# x = [ranges[0],ranges[1]]
# x = [6540,6750]
# y = [ranges[2],ranges[3]]
# #y = [-70,-20]
# #x.reverse()
# ranges = concatenate((x,y))
# axis(ranges)
# grid()
# 
# outname = name[0]+'_'+str(num)+'.png'
##savefig(outname)

show()
