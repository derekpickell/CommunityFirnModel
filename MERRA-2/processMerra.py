import xarray as xr 
import numpy as np
import matplotlib.pyplot as plt
import glob
import datetime

# def year_fraction(date):
#     start = datetime.date(date.year, 1, 1).toordinal()
#     year_length = datetime.date(date.year+1, 1, 1).toordinal() - start
#     return date.year + float(date.toordinal() - start) / year_length +.0833

# # TPSNOW - snow temperature, PRECSNOLAND - total snow, PRECTOTLAND - total precip, EVLAND - evap, SMLAND - snow melt

# lat = 72.61425; lon = -38.28335

# merra_files = sorted(glob.glob('*nc4'))
# # print(merra_files)

# times = []
# for file in merra_files:
#     ds = xr.open_dataset(file)
#     value = ds['time'].values[0]
#     dto = datetime.datetime.strptime(value.astype(str)[:-3], '%Y-%m-%dT%H:%M:%S.%f')
#     decimal_time = year_fraction(dto)
#     times.append(decimal_time)

# rains = []; snows = []; surface_temp = []; east_stress = []; north_stress = []; evaps = []
# for file in merra_files:
#     ds = xr.open_dataset(file)

#     # snowfall - good
#     snow = ds['PRECSNO'] 
#     point_snow = snow.interp(lat=lat, lon=lon, method='linear').values[0] *31536000/917
#     snows.append(point_snow)

#     # skin temp - good
#     skin = ds['TSH']
#     point_skin = skin.interp(lat=lat, lon=lon, method='linear')
#     surface_temp.extend(point_skin)

example = np.genfromtxt('/Users/f005cb1/Documents/Github/CommunityFirnModel/CFM_main/CFMinput_example/example_BDOT.csv', delimiter=',')     
example_times = example[0]
example_data = example[1]

# plt.plot(times, surface_temp, c='r')
plt.plot(example_times, example_data, c='b')
plt.show()