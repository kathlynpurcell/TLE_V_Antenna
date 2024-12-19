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
import matplotlib.dates as mdates
from skyfield.api import load, EarthSatellite

earth_radius_km = 6371.0

def plot_ex():
	## example plot of dummy data
	data=[]
	data_0 = [0]*10
	for i in range(10): data.append(i)
	plt.plot(data,data_0)
	plt.show()

def get_and_load_fits(file):
	## take the file name and get the relevant TLE data
	## return: the TLE data in a list of strings
	#header = Table.read(file, hdu="Primary")
	table = Table.read(file, hdu="ANTPOSPF")
	return table

def plot_FITS(table):
	# subsample the FITS data
	table = table[::100]
	# convert from MJD to utc time
	time_utc = Time(table['DMJD'], format="mjd").datetime
	# plot mnt and obsc AZ values
	plt.plot(time_utc, table['MNT_AZ'], label="MNT AZ")
	plt.plot(time_utc, table['OBSC_AZ'], label="OBSC AZ")
	# format the title, axis and legend
	plt.title("Just FITS for "+ str(time_utc[0].date()))
	xformatter = mdates.DateFormatter('%H:%M')
	plt.gcf().axes[0].xaxis.set_major_formatter(xformatter)
	plt.ylabel("AZ (Deg)")
	plt.xlabel("Time (UTC)")
	plt.legend()
	# plot it
	plt.show()


def main():
	#example
	#plot_ex()

	## provide the satelite name, and pass to the functions
	FITS_file = "SV160.fits"

	FITS = get_and_load_fits(FITS_file)
	plot_FITS(FITS)


if __name__=="__main__":
    main()