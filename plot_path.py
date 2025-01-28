import math
from skyfield.api import load, wgs84

earth_radius_km = 6371.0


TLE_weblink = "https://celestrak.org/NORAD/elements/supplemental/sup-gp.php?FILE=iridium&FORMAT=tle"
ts = load.timescale()


satellites = load.tle_file(TLE_weblink)
by_name = {sat.name: sat for sat in satellites}


# conpute the az and alt from GBO
#bluffton = wgs84.latlon(+38.4195, -79.8318)
bluffton = wgs84.latlon(+38.436850, -79.825518)

t0 = ts.utc(2025, 1, 28, 8, 20, 00)
t1 = ts.utc(2025, 1, 28, 8, 40, 00)

for sat_name in by_name:
	satellite =  by_name[sat_name]
	t, events = satellite.find_events(bluffton, t0, t1, altitude_degrees=15.0)
	event_names = 'rise above 15°', 'culminate', 'set below 15°'
	for ti, event in zip(t, events):
	    name = event_names[event]
	    print(ti.utc_strftime('%Y %b %d %H:%M:%S'), sat_name, name)