__author__ = 'nnyegaard'

import matplotlib.pyplot as plt
import numpy as np
from mpl_toolkits.basemap import Basemap
import json

try:
    with open("../Lecture02/sea_photo_list.txt", "r") as f:
        sea_data = f.read()
except IOError as e:
    print e

lon = []
lat = []

for i in json.loads(sea_data):
    lon.append(i["longitude"])
    lat.append(i["latitude"])




# set up orthographic map projection with
# perspective of satellite looking down at 50N, 100W.
# use low resolution coastlines.
m = Basemap(llcrnrlon=7, llcrnrlat=54, urcrnrlon=13, urcrnrlat=58, projection='cass', lat_0=57, lon_0=10, resolution='i')

m.drawcoastlines()
m.fillcontinents(color='white', lake_color='lightgrey')
# draw parallels and meridians. Lines on the map
m.drawparallels(np.arange(-40, 61., 2.))
m.drawmeridians(np.arange(-20., 21., 2.))
m.drawmapboundary(fill_color='lightgrey')
plt.title("Cassini Projection")

plt.hexbin(lon, lat, extent=(7, 12, 55, 60))
plt.show()