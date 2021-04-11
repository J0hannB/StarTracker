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

R_z = np.matrix(           [[ math.cos(math.radians(lon)), math.sin(math.radians(lon)), 0.0],
                            [-math.sin(math.radians(lon)), math.cos(math.radians(lon)), 0.0],
                            [ 0.0,                         0.0,                         1.0]])

#R_x = np.matrix(           [[1.0,  0.0,                         0.0                        ],
#                            [0.0,  math.cos(math.radians(lat)), math.sin(math.radians(lat))],
#                            [0.0, -math.sin(math.radians(lat)), math.cos(math.radians(lat))]])

R_y = np.matrix(           [[math.cos(math.radians(lat)), 0.0, -math.sin(math.radians(lat))],
                            [0.0,                         1.0,  0.0                        ],
                            [math.sin(math.radians(lat)), 0.0,  math.cos(math.radians(lat))]])

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
#iss_pos_unit = orb.get_position(now, normalize=True)[0]
look = orb.get_observer_look(now, lon, lat, alt) # NOTE: lon is first, lat is second!

# for debugging only: 
iss_llh = orb.get_lonlatalt(now)



print("ISS (lat lon alt) = ({}, {}, {})".format(iss_llh[1], iss_llh[0], iss_llh[2]))

#print('ISS unit vector pos: {}'.format(iss_pos_unit))

print('ISS is {} deg east of north and {} degrees above the horizon'.format(look[0], look[1])) 
print(astronomy.sun_zenith_angle(now, lon, lat))

#iss_alt_m = 408000
#iss_rad_m = (earth_rad_m+iss_alt_m)
#iss_pos_m = np.matrix([iss_rad_m*iss_pos_unit[0], iss_rad_m*iss_pos_unit[1], iss_rad_m*iss_pos_unit[2]])

iss_pos_m = lat_lon_to_ecef(iss_llh[1],                     # lat
                            iss_llh[0],                     # lon
                            earth_rad_m+(iss_llh[2]*1000))  # height (m) (need to cvt km to m)

#iss_pos_m = lat_lon_to_ecef(lat+0.01,                     # lat
#                            lon,                     # lon
#                            earth_rad_m)  # height (m) (need to cvt km to m)
obs_pos_m = lat_lon_to_ecef(lat, lon)

#print('Unit pos: {}'.format(iss_pos_unit))
print('ECEF pos: {} m'.format(iss_pos_m))
print('obs ECEF pos: {} m'.format(obs_pos_m))

d_pos_m = iss_pos_m - obs_pos_m

#TODO: remove
#d_pos_m = np.matrix([earth_rad_m, 0, earth_rad_m] )

#R_ECEF_to_UEN = R_x*R_z 
#R_ECEF_to_UEN = R_y*-R_z 
#d_pos_UEN = R_ECEF_to_UEN*d_pos_m.T # Why isn't transpose working? 
d_pos_NED = R_ECEF_to_NED*d_pos_m.T # Why isn't transpose working? 


# add Earth's radius b/c we are on earth's surface (should eventually compensate for elevation above sea level)
#d_pos_NED[2] += earth_rad_m

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


