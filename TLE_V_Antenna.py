## In this prgram, we want to take data from a local TLE and plot its path

# helpful links
# TLEs https://celestrak.org/Norad/elements/table.php?GROUP=iridium&FORMAT=tle
# skyfield docs https://rhodesmill.org/skyfield/earth-satellites.html#loading-a-single-tle-set-from-strings

from astropy.io import fits
from astropy.table import Table
from astropy.time import Time
from astropy.timeseries import TimeSeries
import numpy as np
import math
import matplotlib.pyplot as plt
import matplotlib.dates as mdates
from skyfield.api import load, EarthSatellite, wgs84
import argparse
import sys

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

	# get metadata
	hdul = fits.open(file)  # open a FITS file
	hdr = hdul[0].header  # the primary HDU header
	metadata = {"OBJECT":hdr["OBJECT"], "PROJID":hdr["PROJID"], "FILE":file}

	return table, time_range, metadata

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
	time_delta = (time_range[-1]-time_range[0]).total_seconds() + ft.second + 10
	# make a skyfield time range from the fits delta
	t = ts.utc(ft.year, ft.month, ft.day, ft.hour, ft.minute, range(ft.second, int(time_delta),10))

	# conpute the az and alt from GBO
	bluffton = wgs84.latlon(+38.4195, -79.8318)
	difference = satellite - bluffton
	topocentric = difference.at(t)
	alt, az, distance = topocentric.altaz()

	return t, az, alt



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

def calc_difference(table, time_range, time, az, el):
	
	return az_difference

def plot_FITS_and_TLE(table, time_range, time, az, el, metadata):
	# plot mnt and obsc AZ values
	plt.subplot(2, 2, 1)
	#plt.plot(time_range, table['MNT_AZ'], label="MNT AZ")
	plt.plot(time_range, table['OBSC_AZ'], label="OBSC AZ")
	# plot TLE date vs TLE AZ
	plt.plot(time.utc_datetime(), az.degrees, label="TLE AZ")
	# format the title, axis and legend
	plt.title("AZ Position: Antenna vs. TLE in Degrees")
	plt.gcf().axes[0].xaxis.set_major_formatter(mdates.DateFormatter('%H:%M'))
	plt.ylabel("AZ (Deg)")
	#plt.xlabel("Time (UTC)")
	# legend
	plt.legend()

	# plot mnt and obsc EL values
	plt.subplot(2, 2, 3)
	#plt.plot(time_range, table['MNT_EL'], label="MNT EL")
	plt.plot(time_range, table['OBSC_EL'], label="OBSC EL")
	# plot TLE date vs TLE AZ
	plt.plot(time.utc_datetime(), el.degrees, label="TLE EL")
	# format the title, axis and legend
	plt.title("EL Position: Antenna vs. TLE in Degrees")
	plt.gcf().axes[1].xaxis.set_major_formatter(mdates.DateFormatter('%H:%M'))
	plt.ylabel("EL (Deg)")
	plt.xlabel("Time (UTC)")
	plt.legend()

	# plot the delta and beam size for AZ
	plt.subplot(2, 2, 2)
	## plot the pos and neg beam size
	data_pos=0.64/np.cos((table['OBSC_EL'])*(math.pi/180))
	data_neg=-0.64/np.cos((table['OBSC_EL'])*(math.pi/180))
	plt.plot(time_range,data_pos,label="Beam Size", c="green")
	plt.plot(time_range,data_neg, c="green")
	plt.title("AZ Beam Size (+/-) and Antenna vs. TLE Difference (Deg)")
	plt.gcf().axes[2].xaxis.set_major_formatter(mdates.DateFormatter('%H:%M'))
	# plot the difference between AZ in Antenna and TLE
	plt.plot(time_range, table['OBSC_AZ']-az.degrees, label="AZ difference")
	plt.legend(borderaxespad=3)

	# plot the delta and beam size for EL
	plt.subplot(2, 2, 4)
	## 
	data=[0.64]*len(time_range)
	plt.plot(time_range,data,label="Beam Size", c="green")
	plt.plot(time_range,np.negative(data), c="green")
	plt.title("EL Beam Size (+/-) and Antenna vs. TLE Difference (Deg)")
	plt.gcf().axes[3].xaxis.set_major_formatter(mdates.DateFormatter('%H:%M'))
	# plot the difference between EL in Antenna and TLE
	plt.plot(time_range, table['OBSC_EL']-el.degrees, label="EL difference")
	plt.xlabel("Time (UTC)")
	plt.legend(borderaxespad=3)


	# plot it
	plt.suptitle("FITS and TLE for "+ metadata["PROJID"]+"\n Date: "
		+str(time_range[0].date())+"   Source: "+metadata["OBJECT"]+"\nFile: "+metadata["FILE"])
	plt.show()

def parser_args(args):
	parser = argparse.ArgumentParser()
	parser.add_argument(
	    "-f",
	    "--fits",
	    type=str,
	    help="Path to fits file with Antenna position data",
	)
	parser.add_argument(
	    "-t",
	    "--tle",
	    type=str,
	    help="Path to TLE file with projected satelite position data",
	)

	args = parser.parse_args()

	return args

def main():
	# example
	#plot_ex()

	## get the file names from the command line (later, crontab)
	#testing command: python TLE_V_Antenna.py -f SV160.fits -t SV160_TLE
	if len(sys.argv) == 1:
	        sys.argv.append("-h")
	args = parser_args(sys.argv)
	FITS_file = args.fits
	TLE_file = args.tle

	# load the data
	FITS, time_range, metadata = get_and_load_fits(FITS_file)
	TLE = get_TLE(TLE_file)
	time, az, el = calculate_TLE(TLE_file, TLE, time_range)

	# plot the data
	#plot_FITS(FITS, time_range)
	#plot_TLE(time, az, time_range)
	plot_FITS_and_TLE(FITS, time_range, time, az, el, metadata)

if __name__=="__main__":
    main()