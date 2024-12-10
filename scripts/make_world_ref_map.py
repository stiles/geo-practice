import matplotlib.pyplot as plt
import cartopy.crs as ccrs
import cartopy.feature as cfeature
from matplotlib.ticker import MultipleLocator, FuncFormatter

# Create a map with Web Mercator projection
fig, ax = plt.subplots(
    figsize=(12, 6),
    subplot_kw={'projection': ccrs.Mercator()}
)

# Clip out the poles
# ax.set_extent([-180, 180, -60, 70], crs=ccrs.PlateCarree())

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
ax.add_feature(cfeature.STATES, edgecolor='white', linewidth=0.5)

# Add coastlines
ax.coastlines()

# Use a grid with numeric labels
gl = ax.gridlines(
    draw_labels=True,
    linewidth=0.4,
    color='gray',
    alpha=0.7,
    linestyle='--'
)
gl.xlocator = MultipleLocator(10)  # Longitude grid every 10 degrees
gl.ylocator = MultipleLocator(5)  # Latitude grid every 5 degrees
gl.xlabel_style = {'size': 10, 'color': 'black'}
gl.ylabel_style = {'size': 10, 'color': 'black'}

# Remove degree symbols and directional labels
gl.xformatter = FuncFormatter(lambda x, _: f'{x:.0f}')
gl.yformatter = FuncFormatter(lambda y, _: f'{y:.0f}')

# Add title
plt.title("Map of the Contiguous United States (CONUS) with States", fontsize=14)

# Show the plot
plt.show()
