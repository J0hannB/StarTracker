#import httpInterface as http
from pyorbital.orbital import Orbital
from pyorbital import astronomy
from datetime import datetime
import math
import numpy as np

earth_rad_m = 6.371e6

def lat_lon_to_ecef(lat, lon, height=earth_rad_m): 
    x = height*math.sin(math.radians(90 - lat))*math.cos(math.radians(lon))
    y = height*math.sin(math.radians(90 - lat))*math.sin(math.radians(lon))
    z = height*math.cos(math.radians(90 - lat))
    return np.matrix([x, y, z])


lat, lon, alt = 29.76, -95.36, 0

lat_rad = math.radians(lat)
lon_rad = math.radians(lon)

R_ECEF_to_NED = np.matrix([
                            [-math.sin(lat_rad)*math.cos(lon_rad), -math.sin(lat_rad)*math.sin(lon_rad),  math.cos(lat_rad)],
                            [-math.sin(lon_rad),                    math.cos(lon_rad),                    0                ],
                            [-math.cos(lat_rad)*math.cos(lon_rad), -math.cos(lat_rad)*math.sin(lon_rad), -math.sin(lat_rad)] 
                          ])
#iss_sat_num = 25544
orb = Orbital('ISS (ZARYA)')
now = datetime.utcnow()
look = orb.get_observer_look(now, lon, lat, alt) # NOTE: lon is first, lat is second!
iss_llh = orb.get_lonlatalt(now)

print("ISS (lat lon alt) = ({}, {}, {})".format(iss_llh[1], iss_llh[0], iss_llh[2]))
print('ISS is {} deg east of north and {} degrees above the horizon'.format(look[0], look[1])) 
#print(astronomy.sun_zenith_angle(now, lon, lat))

iss_pos_m = lat_lon_to_ecef(iss_llh[1],                     # lat
                            iss_llh[0],                     # lon
                            earth_rad_m+(iss_llh[2]*1000))  # height (m) (need to cvt km to m)

obs_pos_m = lat_lon_to_ecef(lat, lon)

print('ECEF pos: {} m'.format(iss_pos_m))
print('obs ECEF pos: {} m'.format(obs_pos_m))

d_pos_m = iss_pos_m - obs_pos_m
d_pos_NED = R_ECEF_to_NED*d_pos_m.T

print("d pos ECEF {} m".format(d_pos_m))
print("d pos NED {} m".format(d_pos_NED))

d_pos_yz = np.matrix([0, d_pos_NED.item(1), d_pos_NED.item(2)]) 

print("d_pos_yz: {} m".format(d_pos_yz))

dot_product = np.inner(d_pos_yz, np.matrix([0, 0, 1]))
print("dot product: {}".format(dot_product))

x_angle_rad = np.arccos(dot_product/(np.linalg.norm(d_pos_NED, axis=0)))

print("x angle: {}".format(np.degrees(x_angle_rad)))

z_angle_rad = np.arcsin(d_pos_NED[2]/np.linalg.norm(d_pos_NED, axis=0))

print("z angle: {}".format(np.degrees(z_angle_rad)))


