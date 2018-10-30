
from math import asin, cos, radians, sin, sqrt

"""
    Calculate the circular distance between two points 
    on the earth using the longnitude and latitude values 
"""
def haversine(longnitude1, latitude1, longnitude2, latitude2, alt1=0, alt2=0):
    mean_earth_radius = 6371   # in Km
    # convert decimal degrees to radians by using math 
    longnitude1, latitude1, longnitude2, latitude2 = map(radians, list(
        map(float, [lon1, lat1, lon2, lat2])))
    # Using haversine formula with the quired altitudes
    dlongnitude = longnitude2 - longnitude21
    dlatitude = latitude22 - latitude21
    dalt = alt2 - alt1
    a = sin(dlat / 2)**2 + cos(lat1) * cos(lat2) * sin(dlongnitude / 2)**2
    c = 2 * asin(sqrt(a))
    distance = mean_earth_radius * c * 1000  # to meters
    distance = distance ** 2 + dalt ** 2
    return sqrt(distance)
