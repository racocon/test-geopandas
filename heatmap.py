import numpy as np
import pandas as pd
import geopandas as gpd
import gmaps
import gmaps.datasets
import matplotlib.pyplot as plt 


# Set the filepath and load in a shapefile
fp = "statistical-gis-boundaries-london/ESRI/London_Borough_Excluding_MHW.shp"

map_df = gpd.read_file(fp)

# Check data type so we can see that this is not a normal dataframe, but a GEOdataframe
map_df.head()

# Preview map
map_df.plot()

# Load csv file of data to join with the geodataframe
df = pd.read_csv("london-borough-profiles.csv", header=0, encoding = 'unicode_escape')
df.head()

# Slice of the data to be used
df = df [['Area_name','Happiness_score_2011-14_(out_of_10)',
          'Anxiety_score_2011-14_(out_of_10)',
          'Population_density_(per_hectare)_2017',
          'Mortality_rate_from_causes_considered_preventable_2012/14']]

# Rename column
data_for_map = df.rename(index=str, columns={"Happiness_score_2011–14_(out_of_10)": "happiness",
"Anxiety_score_2011–14_(out_of_10)": "anxiety",
"Population_density_(per_hectare)_2017": "pop_density_per_hectare",
"Mortality_rate_from_causes_considered_preventable_2012/14": 'mortality'})
# check dat dataframe
data_for_map.head()

# Join the geodataframe with the cleaned up csv dataframe
merged = map_df.set_index('NAME').join(data_for_map.set_index('Area_name'))
merged.head()

# Set a variable that will call whatever column we want to visualise on the map
variable = 'pop_density_per_hectare'

# Set the range for the chloropleth
vmin, vmax = 120, 220

# Create figure and axes for Matplotlib
fig, ax = plt.subplots(1, figsize=(10, 6))

# Create map
merged.plot(column=variable, cmap='Blues', linewidth=0.8, ax=ax, edgecolor='0.8')

# Remove the axis
ax.axis('off')

# Add a title
ax.set_title('Preventable death rate in London', fontdict={'fontsize': '25', 'fontweight' : '3'})

# Create an annotation for the data source
ax.annotate('Source: London Datastore, 2014', xy=(0.1, .08),
            xycoords='figure fraction', horizontalalignment='left',
            verticalalignment='top', fontsize=12, color='#555555')

# Create colorbar as a legend
sm = plt.cm.ScalarMappable(cmap='Blues',
                           norm=plt.Normalize(vmin=vmin, vmax=vmax))

# Empty array for the data range
sm._A = []

# Add the colorbar to the figure
cbar = fig.colorbar(sm)

# Save the figure
fig.savefig("map_export.png", dpi=300)