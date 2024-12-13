import xarray as xr 
import numpy as np
import matplotlib.pyplot as plt
import glob
import datetime
import csv

def year_fraction(date):
    start = datetime.date(date.year, 1, 1).toordinal()
    year_length = datetime.date(date.year+1, 1, 1).toordinal() - start
    return date.year + float(date.toordinal() - start) / year_length +.0833

# TPSNOW - snow temperature, PRECSNOLAND - total snow, PRECTOTLAND - total precip, EVLAND - evap, SMLAND - snow melt

lat = 72.61425; lon = -38.28335
# lat = 30.61425; lon = -40.28335


merra_files = sorted(glob.glob('*nc4'))
# print(merra_files)

times = []
for file in merra_files:
    ds = xr.open_dataset(file)
    value = ds['time'].values[0]
    dto = datetime.datetime.strptime(value.astype(str)[:-3], '%Y-%m-%dT%H:%M:%S.%f')
    decimal_time = year_fraction(dto)
    times.append(decimal_time)

rains = []; snows = []; surface_temp = []; east_stress = []; north_stress = []; evaps = []
for file in merra_files:
    ds = xr.open_dataset(file)

    # snowfall 
    # snow = ds['PRECSNOLAND']
    # point_snow = snow.interp(lat=lat, lon=lon, method='linear').values[0] *31536000/917
    # snows.append(point_snow)

    # skin temp 
    skin = ds['SMLAND']
    point_skin = skin.interp(lat=lat, lon=lon, method='linear').values
    print(max(point_skin)); exit()
    surface_temp.extend(point_skin)

example = np.genfromtxt('/Users/f005cb1/Documents/Github/CommunityFirnModel/CFM_main/CFMinput_example/example_TSKIN.csv', delimiter=',')     
example_times = example[0]
example_data = example[1]

print(surface_temp)
plt.plot(times, surface_temp, c='r')
plt.plot(example_times, example_data, c='b')
plt.show()

# SAVE FILES
def write_csv(list1, list2, filename):
    with open(filename, mode="w", newline="") as file:
        writer = csv.writer(file)
        writer.writerow(list1)  # Write the top row
        writer.writerow(list2)  # Write the bottom row

def extend_data(list1, list2, start_year, repeat_year_start=1980.0833, repeat_year_end=1999.9167):
    start_index = min(range(len(list1)), key=lambda i: abs(list1[i] - repeat_year_start))
    end_index = min(range(len(list1)), key=lambda i: abs(list1[i] - repeat_year_end))
    print(f"indices found: {list1[start_index]}, {list1[end_index]}")
    print(f"CHECK dates prior to start: {list1[start_index-1]}, {list1[end_index+1]}")
    