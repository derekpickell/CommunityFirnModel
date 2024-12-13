import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import csv

density_file_path = './SUMup_2024_density_csv/SUMup_2024_density_greenland.csv'

density_data = pd.read_csv(density_file_path)
summit_density_data = density_data[(density_data.latitude > 72) & (density_data.latitude < 73) & 
                                   (density_data.longitude > -39) & (density_data.longitude < -37)]
unique_keys = summit_density_data.profile_key.unique()
unique_depths = sorted(summit_density_data.midpoint.unique())

fig, ax = plt.subplots()
interpolated_densities = []
for key in unique_keys: 
    filtered_subset = summit_density_data[summit_density_data.profile_key == key]
    midpoints = filtered_subset.midpoint.tolist()
    densities =  filtered_subset.density.tolist()
    midpoints, densities = zip(*sorted(zip(midpoints, densities)))
    date = filtered_subset.timestamp.iloc[0]
    dataset_key = filtered_subset.profile_key.iloc[0]
    ax.plot(densities, midpoints, label=f"dataset {dataset_key} on {date}")

    # for averaging all together
    interpolated_y = np.interp(unique_depths, midpoints, densities, left=np.nan, right=np.nan)
    interpolated_densities.append(interpolated_y)

average_density = np.nanmean(interpolated_densities, axis=0)
interpolated_depths = np.arange(0, 330+.1, .1)
interpolated_avg_density = np.interp(interpolated_depths, unique_depths, average_density)
interpolated_avg_density = [x for x in interpolated_avg_density if x < 917 ]
interpolated_depths = interpolated_depths[0:len(interpolated_avg_density)]
ax.plot(interpolated_avg_density, interpolated_depths, label="Average", lw=5, color='black')

ax.set_ylabel("Depth below surface [m - midpoint]")
ax.set_xlabel("Density (kg/m^3)")
ax.invert_yaxis()
ax.legend(fontsize='5', ncol=2)
fig.suptitle("Densities From Summit Vicinity (72-73N, 38-36W)")
# plt.show()

with open("Summit_avg_density_profile.csv", "w", newline="") as csvfile:
    writer = csv.writer(csvfile)
    
    # Write the header
    writer.writerow(["depth", "density"])
    
    # Write the data
    for d, dens in zip(interpolated_depths, interpolated_avg_density):
        writer.writerow([d, dens])

print("Data saved in csv.'")