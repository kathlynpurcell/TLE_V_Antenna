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
from skyfield.api import load, EarthSatellite, wgs84

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
	
	# get and subsample the FITS data
	table = Table.read(file, hdu="ANTPOSPF")[::100]
	
	# convert from MJD to utc time
	time_range = Time(table['DMJD'], format="mjd").datetime

	return table, time_range

def plot_FITS(table, time_range):
	# plot mnt and obsc AZ values
	plt.plot(time_range, table['MNT_AZ'], label="MNT AZ")
	plt.plot(time_range, table['OBSC_AZ'], label="OBSC AZ")

	# format the title, axis and legend
	plt.title("Just FITS for "+ str(time_range[0].date()))
	xformatter = mdates.DateFormatter('%H:%M')
	plt.gcf().axes[0].xaxis.set_major_formatter(xformatter)
	plt.ylabel("AZ (Deg)")
	plt.xlabel("Time (UTC)")
	plt.legend()

	# plot it
	plt.show()

def get_TLE(file):
	## take the file name and get the relevant TLE data
	with open(file) as f:
	    TLE = [line.rstrip() for line in f]
	f.close()
	return TLE
	
def calculate_TLE(file, TLE, time_range):
	## convert the TLE string into a skyfield object
	## return: time range and positions
	ts = load.timescale()
	satellite = EarthSatellite(TLE[1], TLE[2], file, ts)

	# find the FITS time delta
	ft = time_range[0]
	time_delta = (time_range[-1]-time_range[0]).total_seconds()
	# make a skyfield time range from the fits delta
	t = ts.utc(ft.year, ft.month, ft.day, ft.hour, ft.minute, range(0,int(time_delta),10))

	# conpute the az and alt from GBO
	bluffton = wgs84.latlon(+38.4195, -79.8318)
	difference = satellite - bluffton
	topocentric = difference.at(t)
	alt, az, distance = topocentric.altaz()

	return t, az



def plot_TLE(time, az, time_range):
	## plot just the TLE
	## result: matplotlib plot of TLE path v. time

	# plot TLE date vs TLE AZ
	plt.plot(time.utc_datetime(), az.degrees, label="TLE AZ")

	# formatting title, axis and legend
	plt.title("Just TLE for "+ str(time_range[0].date()))
	xformatter = mdates.DateFormatter('%H:%M')
	plt.gcf().axes[0].xaxis.set_major_formatter(xformatter)
	plt.ylabel("AZ (Deg)")
	plt.xlabel("Time (UTC)")
	plt.legend()

	# plot it
	plt.show()

def plot_FITS_and_TLE(table, time_range, time, az):
	# plot mnt and obsc AZ values
	plt.plot(time_range, table['MNT_AZ'], label="MNT AZ")
	plt.plot(time_range, table['OBSC_AZ'], label="OBSC AZ")

	# plot TLE date vs TLE AZ
	plt.plot(time.utc_datetime(), az.degrees, label="TLE AZ")

	# format the title, axis and legend
	plt.title("FITS and TLE for "+ str(time_range[0].date()))
	xformatter = mdates.DateFormatter('%H:%M')
	plt.gcf().axes[0].xaxis.set_major_formatter(xformatter)
	plt.ylabel("AZ (Deg)")
	plt.xlabel("Time (UTC)")

	plt.legend()

	# plot it
	plt.show()

def main():
	# example
	#plot_ex()

	## provide the satelite name, and pass to the functions
	FITS_file = "SV160.fits"
	TLE_file = "SV160_TLE"

	# load the data
	FITS, time_range = get_and_load_fits(FITS_file)
	TLE = get_TLE(TLE_file)
	time, az = calculate_TLE(TLE_file, TLE, time_range)

	# plot the data
	#plot_FITS(FITS, time_range)
	#plot_TLE(time, az, time_range)
	plot_FITS_and_TLE(FITS, time_range, time, az)

if __name__=="__main__":
    main()