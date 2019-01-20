import math


def dist(lat1, lat2, long1, long2):
    lat_in_met = 111403.03571168562
    long_in_met = 56704.740688511745
    return math.sqrt((lat_in_met * (lat1 - lat2)) ^ 2 +
                     (long_in_met * (long1 - long2) ^ 2))


default_range = 64
