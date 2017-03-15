import matplotlib.pyplot as plt
import numpy as np
from astropy.io import fits
import pyspeckit

datfile =  fits.open('filename')
hdr = datfile[1].header

"Kelle was here"
"Kelle is up to no good"


#try:
#        data = datfile[1].data
#    except IndexError:
#        pass
#    else:
#        good = False
        names = datfile[1].dtype.names
        if 'loglam' in  names and 'flux' in names:
            flux = datfile[1].data['flux']
            wlen = 10**np.array(datflike[1].data['loglam'])
            indx = np.where((wlen > 8250) & (wlen < 8350))
            avgval = flux[indx].mean()
            nflux = flux/avgval

        #    good = True
        #elif 'wavelength' in names and 'flux' in names:
        #    wa = data.wavelength
        #    fl = data.flux
        #    good = True
        #if good:
        #    er = np.ones_like(flux)
        #    try:
        #        err = datfile[1].data['ivar']
        #    except AttributeError:
        #        pass
        #    co = np.empty_like(fl) * np.nan
        #    try:
        #        co = data.co
        #    except AttributeError:
        #        pass
        #    return Spectrum(wa=wa, fl=fl, er=er, co=co, filename=filename)
#
