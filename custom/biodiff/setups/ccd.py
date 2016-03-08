# -*- coding: utf-8 -*-

description = "Andor DV936 CCD camera setup"
group = "basic"

includes = ["shutter", "microstep", "reactor", "nl1", "guidehall", "astrium"]

tango_base = "tango://phys.biodiff.frm2:10000/biodiff/"
tango_ikonl = tango_base + "detector/ikonl"
tango_limaccd = tango_base + "detector/limaccd"

devices = dict(
    FITSFileSaver = device("devices.fileformats.fits.FITSFileFormat",
                           description = "Saves image data in FITS format",
                           filenametemplate = ["%(proposal)s_%(counter)08d"
                                               ".fits"],
                          ),
    ccdtime = device("devices.vendor.lima.LimaCCDTimer",
                     description = "Internal LimaCDDTimer",
                     tangodevice = tango_limaccd,
                     ),
    ccd     = device("devices.vendor.lima.Andor2LimaCCD",
                     description = "Andor DV936 CCD camera",
                     tangodevice = tango_limaccd,
                     hwdevice = tango_ikonl,
                     maxage = 10,
                     bin = (2, 2),
                     flip = (False, False),
                     rotation = 0,
                     vsspeed = 76.95,
                     hsspeed = 1,
                     pgain = 4,
                    ),
    ccddet  = device("biodiff.detector.BiodiffDetector",
                     description = "Andor DV936 CCD detector",
                     timers = ["ccdtime"],
                     images = ["ccd"],
                     maxage = 10,
                     fileformats = ["FITSFileSaver"],
                     gammashutter = "gammashutter",
                     photoshutter = "photoshutter",
                     subdir = ".",
                    ),
    ccdTemp = device("devices.vendor.lima.Andor2TemperatureController",
                     description = "Andor DV936 CCD temperature control",
                     tangodevice = tango_ikonl,
                     maxage = 5,
                     abslimits = (-100, 0),
                     userlimits = (-100, 0),
                     unit = 'degC',
                     precision = 3,
                     fmtstr = '%.0f',
                    ),
)

startupcode = '''
SetDetectors(ccddet)
'''
