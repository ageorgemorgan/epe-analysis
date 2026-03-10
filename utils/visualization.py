import cartopy.crs as ccrs
from cartopy.mpl.ticker import LatitudeFormatter, LongitudeFormatter
import numpy as np
import matplotlib.pyplot as plt

def draw_global_map(
    lon,
    lat,
    field_vals,
    title = None,
    filled = False,
    show_fig = True,
    save_fig = False,
    levels = 8,
    cmap = "plasma",
    cbar_params = [0.95, 0.2, 0.05, 0.6],
    bbox = None,
    vmin = None,
    vmax = None,
    draw_labels = False,
    label_contours = False,
    remove_cbar = False,
    fig = None,
    projection = ccrs.Miller(central_longitude=180),
    outfilename = "my_map" + ".png",
):
    """
    Produces a (possibly filled) contour plot of a scalar field with gridded lat/lon values
    "field_vals" overlaid on a global map.

    Note in particular that the input data *must* be in lat/lon ie Plate-Carree
    """
    # Draw annotated map
    if fig is None:
        fig, ax = plt.subplots(
            1,
            1,
            figsize=(8, 6),
            subplot_kw={"projection": projection}
        )

    else:
        ax = fig.subplots(
            1,
            subplot_kw={"projection": projection}
        )

    ax.set_global()
    ax.coastlines()

    gl = ax.gridlines(draw_labels = draw_labels, crs = projection, linestyle="--")
    gl.top_labels = False
    gl.right_labels = False

    # Tick labels thanks to this nice post:
    # https://stackoverflow.com/questions/61577057/weird-setting-of-latitude-labels-in-cartopy-miller-projection
    ax.set_xticks(np.arange(-180, 180, 60), crs = ccrs.PlateCarree())
    ax.set_yticks(np.arange(-90, 90.5, 30), crs = ccrs.PlateCarree())
    lat_formatter = LatitudeFormatter()
    lon_formatter = LongitudeFormatter()
    ax.yaxis.set_major_formatter(lat_formatter)
    ax.xaxis.set_major_formatter(lon_formatter)
    plt.xticks(fontsize = 13)
    plt.yticks(fontsize = 13)

    # Draw contour plot
    my_levels = np.linspace(vmin, vmax, levels + 1, endpoint=True) if (
                vmin is not None and vmax is not None
    ) else levels

    if filled:
        co = ax.contourf(
            lon,
            lat,
            field_vals,
            transform = ccrs.PlateCarree(),
            levels = my_levels,
            cmap = cmap,
            vmin = vmin,
            vmax = vmax,
        )

    else:
        co = ax.contour(
            lon,
            lat,
            field_vals,
            transform = ccrs.PlateCarree(),
            levels = my_levels,
            cmap = cmap,
            vmin = vmin,
            vmax = vmax,
        )

    # Label the contours on the plot if desired.
    # We don't allow contour labels if we're drawing a filled plot!
    if not filled and label_contours:
        ax.clabel(co, co.levels, fontsize = 13)

    # Title
    if title:
        plt.title(title, fontsize = 16)

    # Draw colorbar
    cbar_ax = fig.add_axes(cbar_params)
    cbar = plt.colorbar(co, cax=cbar_ax)
    cbar.ax.tick_params(labelsize = 13)

    if vmin is not None and vmax is not None:
        cbar.mappable.set_clim(vmin, vmax)

    # Remove colorbar if desired
    if remove_cbar:
        cbar.remove()

    # Zoom in if required
    if bbox is not None:
        ax.set_extent(bbox)

    # Save and/or display the figure
    if save_fig:
        plt.savefig(
            "images/" + outfilename,
            dpi = 600,
            bbox_inches = "tight",
        )

    if show_fig:
        plt.show()

    return None