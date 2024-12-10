import matplotlib.pyplot as plt
import cartopy.crs as ccrs
import cartopy.feature as cfeature
from cartopy.io.shapereader import natural_earth, Reader
import geopandas as gpd
from matplotlib.ticker import MultipleLocator, FuncFormatter
from cartopy.feature import ShapelyFeature

# Create a map with Web Mercator projection
fig, ax = plt.subplots(
    figsize=(12, 6),
    subplot_kw={'projection': ccrs.Mercator()}
)

# Set the extent for the contiguous United States (CONUS)
ax.set_extent([-125, -66.5, 24, 49.5], crs=ccrs.PlateCarree())

# Add countries with light gray fill and white borders
countries = cfeature.NaturalEarthFeature(
    category='cultural',
    name='admin_0_countries',
    scale='110m',
    facecolor='lightgray',
    edgecolor='white'
)
ax.add_feature(countries, zorder=0)

# Add U.S. states with white borders
states_shp_path = natural_earth(
    resolution='50m',
    category='cultural',
    name='admin_1_states_provinces'
)
us_states = gpd.read_file(states_shp_path)
us_states = us_states[us_states['iso_a2'] == 'US']

# Add state names
for _, row in us_states.iterrows():
    print(row)
    ax.text(
        row['geometry'].centroid.x,
        row['geometry'].centroid.y,
        row['iso_3166_2'].replace('US-', ''),
        transform=ccrs.PlateCarree(),
        fontsize=8,
        color='black',
        weight='bold',
        ha='center',
        va='center'
    )

# Add state boundaries without fill
ax.add_feature(
    ShapelyFeature(
        Reader(states_shp_path).geometries(),
        ccrs.PlateCarree()
    ),
    edgecolor='white',
    facecolor='none',  # No fill for state boundaries
    linewidth=0.5
)

# Use a grid with numeric labels
gl = ax.gridlines(
    draw_labels=True,
    linewidth=0.4,
    color='gray',
    alpha=0.7,
    linestyle='--'
)
gl.xlocator = MultipleLocator(5)  # Longitude grid every 10 degrees
gl.ylocator = MultipleLocator(5)  # Latitude grid every 5 degrees
gl.xlabel_style = {'size': 10, 'color': 'black'}
gl.ylabel_style = {'size': 10, 'color': 'black'}

# Remove degree symbols and directional labels
gl.xformatter = FuncFormatter(lambda x, _: f'{x:.0f}')
gl.yformatter = FuncFormatter(lambda y, _: f'{y:.0f}')

# Add title
plt.title("Map of the Contiguous United States (CONUS) with State Names", fontsize=14)

# Show the plot
plt.show()
