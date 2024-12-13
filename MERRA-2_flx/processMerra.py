import xarray as xr 
import numpy as np
import matplotlib.pyplot as plt
import glob
import datetime
import csv

# INPUT MERRA-2 SUBSET COORDINATES: - -40,71,-36,74

def year_fraction(date):
    start = datetime.date(date.year, 1, 1).toordinal()
    year_length = datetime.date(date.year+1, 1, 1).toordinal() - start
    return date.year + float(date.toordinal() - start) / year_length +.0833

# TPSNOW - snow temperature, PRECSNOLAND - total snow, PRECTOTLAND - total precip, EVLAND - evap, SMLAND - snow melt

lat = 72.61425; lon = -38.28335

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

    # snowfall - good
    snow = ds['PRECSNO'] 
    point_snow = snow.interp(lat=lat, lon=lon, method='linear').values[0] *31536000/917
    snows.append(point_snow)

    # skin temp - good
    skin = ds['TSH']
    point_skin = skin.interp(lat=lat, lon=lon, method='linear')
    surface_temp.extend(point_skin)

    # rains - mostly good. No 2021 rain??
    total_precip = ds['PRECTOT']
    point_precip = total_precip.interp(lat=lat, lon=lon, method='linear').values[0] *31536000/917
    rain = point_precip - point_snow
    rains.append(rain)

# SAVE FILES
def write_csv(list1, list2, filename):
    with open(filename, mode="w", newline="") as file:
        writer = csv.writer(file)
        writer.writerow(list1)  # Write the top row
        writer.writerow(list2)  # Write the bottom row

def extend_data(list1, list2, start_year, repeat_year_start=1981.99836849, repeat_year_end=1989.99836849):
    list1 = np.array(list1)
    list2 = np.array(list2)
    
    # Find indices closest to the start and end of the repeat year range
    start_index = np.argmin(np.abs(list1 - repeat_year_start))
    end_index = np.argmin(np.abs(list1 - repeat_year_end))
    
    print(f"indices found: {list1[start_index]}, {list1[end_index]}")
    if start_index > 0 and end_index + 1 < len(list1):
        print(f"CHECK dates prior to start: {list1[start_index-1]}, {list1[end_index+1]}")
    
    # Calculate the time chunk and how many repetitions are needed
    time_chunk = repeat_year_end - repeat_year_start
    backward_chunks = int((repeat_year_start - start_year) / time_chunk)
    
    # Extract the base ranges
    date_range = list1[start_index:end_index+1]
    data_range = list2[start_index:end_index+1]
    
    # Initialize the final lists with the original data
    final_dates = list1.tolist()  # Include the full original date range
    final_data = list2.tolist()
    
    # Backward extension
    for x in range(1, backward_chunks + 1):
        date_segment = date_range - x * time_chunk
        mask = date_segment < final_dates[0]  # Ensure no overlap with existing data
        final_dates = list(date_segment[mask]) + final_dates
        final_data = list(data_range[mask]) + final_data
    
    return final_dates, final_data
    

example = np.genfromtxt('/Users/f005cb1/Documents/Github/CommunityFirnModel/CFM_main/CFMinput_example/example_TSKIN.csv', delimiter=',')     
example_times = example[0]
example_data = example[1]

# SURFACE TEMPS
final_times, final_temps = extend_data(times, surface_temp, 1450)
write_csv(final_times, final_temps, "1450-2024_Summit_temps.csv")
# plt.plot(final_times, final_temps, c='r')
# plt.plot(example_times, example_data, c='b')
# plt.show()

# SNOW FALL
_, final_snows = extend_data(times, snows, 1450)
write_csv(final_times, final_snows, "1450-2024_Summit_bdot.csv")

# RAINS
_, final_rains = extend_data(times, rains, 1450)
write_csv(final_times, final_rains, "1450-2024_Summit_rain.csv")