import xarray as xr
import matplotlib.pyplot as plt
import numpy as np
import csv
from scipy.integrate import simps

file_path = "CFMoutput_test/csv/CFMresults_Summit1.hdf5"
dataset = xr.open_dataset(file_path, engine="netcdf4")
density = dataset['density']
depth = dataset["depth"]
compaction = dataset["compaction"]
dip = dataset["DIP"]
cumulative_elevation = dip[:,6]
total_compaction = dip[:,4]

compaction_csv = "CFMoutput_test/csv/output_firn_layers.csv"
d1 = np.genfromtxt(compaction_csv, delimiter=',')

# GET VARIABLES
decimal_years = density[:, 0]  # First column: Decimal years
density_values = density[:, 1:]  # Remaining columns: Densities
depths = depth.values[1:] # Remaining values: Depths
single_density_profile = density_values[15]
compaction_values = compaction[:, 1:]
single_compaction_date = compaction_values[15]
decimal_year_values = decimal_years.values
date = decimal_year_values[15]

# PLOT COMPACTION THROUGH TIME, USING DIP VECTOR
# fig, [ax1, ax2] = plt.subplots(2)
# ax1.plot(decimal_year_values[1:], total_compaction[1:])
# total_compaction_cumsum = np.cumsum(total_compaction[1:])
# ax2.plot(decimal_year_values[1:], total_compaction_cumsum)
# ax1.set_ylabel("m")
# ax1.set_title("Total column compaction since last timestep")
# ax2.set_title("Cumulative compaction")
# ax2.set_ylabel("m")
# fig.suptitle("'DIP - total compaction' field ")
# tc = total_compaction_cumsum[-1]/(decimal_year_values[-1] - decimal_year_values[1])
# print(f"Cumulative compaction: {tc} m/yr")
# plt.tight_layout()
# total_compaction_cumsum = total_compaction_cumsum.values.tolist()

# with open("Summit_compaction_velocity.csv", "w", newline="") as csvfile:
#     writer = csv.writer(csvfile)
    
#     # Write the header
#     writer.writerow(["time", "compaction"])
    
#     # Write the data
#     for d, dens in zip(decimal_year_values[1:], total_compaction_cumsum):
#         writer.writerow([d, dens])

total_compactions = total_compaction.values[1:]
compaction_values = compaction_values[1:]
for i in range(0, len(compaction_values)):
    scale_Factor = total_compactions[i]/np.sum(compaction_values[i])
    compaction_values[i] = compaction_values[i]*scale_Factor

# TOTAL COMPACTION THROUGH TIME, USING COMPACTION VARIABLE
fig2, [ax3, ax4] = plt.subplots(2)
d1_compactions_0 = [np.sum(x) for x in d1]
ax3.plot(decimal_year_values[1:], d1_compactions_0, c='black', linestyle='dashed')
d1_compactions_0 = [np.sum(x[0:]) for x in d1]
ax3.plot(decimal_year_values[1:], d1_compactions_0, c='red')
d1_compactions = [np.sum(x[2:]) for x in d1]
ax3.plot(decimal_year_values[1:], d1_compactions, c='orange')
d1_compactions = [np.sum(x[4:]) for x in d1]
ax3.plot(decimal_year_values[1:], d1_compactions, c='green')
d1_compactions = [np.sum(x[6:]) for x in d1]
ax3.plot(decimal_year_values[1:], d1_compactions, c='blue')
d1_compactions = [np.sum(x[8:]) for x in d1]
ax3.plot(decimal_year_values[1:], d1_compactions, c='purple')
ax3.plot(decimal_year_values[1:], total_compaction[1:], c='pink')
ax3.set_ylabel("m")
ax3.set_title("Designated column compaction since last timestep")
total_compaction_cumsum = np.cumsum(d1_compactions_0)
ax4.plot(decimal_year_values[1:], total_compaction_cumsum)
ax4.set_title("Cumulative compaction")
ax4.set_ylabel("m")
fig2.suptitle("'compaction' field total compaction")
print(f"Cumulative compaction: {total_compaction_cumsum[-1]/(decimal_year_values[-1] - decimal_year_values[1])} m/yr")
plt.tight_layout()
plt.show()

# PlOT EXAMPLE DENSITY PROFILE
# plt.plot(single_density_profile, depths)
# plt.title(date)
# plt.ylabel("Depth (m)")
# plt.xlabel("Density (kg/m^3)")
# plt.gca().invert_yaxis() 
# plt.show()



# COMPACTION PROFILE
# x =15
# fiz, az = plt.subplots()
# az.plot(single_compaction_date, depths, c='b')
# ay = az.twiny()
# # compaction_rate = [j/(decimal_year_values[x] - decimal_year_values[x-1]) for j in compaction_values[x]]
# compaction_rate = np.cumsum(compaction_values[15])
# ay.plot(compaction_rate, depths, c='r')
# fiz.suptitle(date)
# az.set_ylabel("Depth (m)")
# az.set_xlabel("Compaction since last timestep(m)")
# ay.set_xlabel("Cumulative compaction with depth")
# plt.gca().invert_yaxis() 
# plt.show()



