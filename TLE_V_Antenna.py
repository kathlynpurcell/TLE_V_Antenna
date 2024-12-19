## In this prgram, we want to take data from a local TLE and plot its path

# helpful links
# TLEs https://celestrak.org/Norad/elements/table.php?GROUP=iridium&FORMAT=tle
# skyfield docs https://rhodesmill.org/skyfield/earth-satellites.html#loading-a-single-tle-set-from-strings

from astropy.io import fits
from astropy.table import Table
from astropy.time import Time
from astropy.timeseries import TimeSeries
import numpy as np
import matplotlib.pyplot as plt
from skyfield.api import load, EarthSatellite

earth_radius_km = 6371.0

def plot_ex():
	## example plot of dummy data
	data=[]
	data_0 = [0]*10
	for i in range(10): data.append(i)
	plt.plot(data,data_0)
	plt.show()


def main():
	#example
	plot_ex()


if __name__=="__main__":
    main()