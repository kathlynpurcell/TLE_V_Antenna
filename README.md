# TLE vs. Antenna Plotting 

A program for plotting antenna reported Azimuth and Elevation values against predicted TLE positions. 

# How to get and use the program

1. Get the program
```bash
    git clone git@github.com:kathlynpurcell/TLE_V_Antenna.git
    cd TLE_V_Antenna
    # make and source a new venv, if on the GBO network do the following
    ~gbosdd/pythonversions/3.11/bin/python -m venv tle_env
    source tle_env/bin/activate
    pip install -U pip setuptools wheel build
    pip install -r requirements.txt
    pip install -e .
```

2.  To run the program

- ex. `$ python TLE_V_Antenna.py -f <fits file> -t <TLE file>`

This will result in a matplotlib popup window of 4 plots, see below for information on the results of these plots. 

# Results of the program

Four plots are produced when running the main python file. 

1. Antenna vs. TLE Azimuth Values
The telescope will report the actual antenna positions when taking data into antenna fits files. These values are intended to follow the predicted path of the satellite given by the TLE calculations. We would like to know how accurately  the telescope was able to maintain position on the source. This is done through comparing the TLE predicted path and the actual path given in the antenna fits file which is presented for the azimuth values in plot #1.

2. Antenna vs. TLE Elevation Values
This plot is the same information as above, but for elevation values. 

3. Azimuth Beam Size vs. Azimuth TLEvAntenna Deltas
This plot presents two sets of data. The first is the delta between the antenna and TLE azimuth data. This is a strict calculation of Antenna - TLE data at each data point (10s intervals)
This also presents the beam size as a function of elevation per the following equation:
Beam Size = (+/-)0.64/cos(elevation)
Where elevation is in degrees and 0.64 (degrees) is wavelength / dish diameter.

4. Elevation Beam Size vs. Azimuth TLEvAntenna Deltas
Plot #4 is the same as plot #3 but for elevation deltas and following the following equation for beam size:
Beam size = (+/-) 0.64
Where 0.64 (degrees) is wavelength / dish diameter.

# Information on the Data Reduction
Antenna Positions are gathered from the fits files in table: ANTPOSPF and columns OBSC_AZ and OBSC_EL there is significant  granularity there so we subsample to a factor of 100.

TLEs are provided and calculated via skyfield EarthSatellite. The length is generated to match the antenna fits length with an interval of 10s, also matching the fits file. Allowing them to be calculated and plotted in tandem.