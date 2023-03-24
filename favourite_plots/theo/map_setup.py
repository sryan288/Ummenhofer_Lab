import xarray as xr
import cartopy.crs as ccrs
import matplotlib as mpl
import matplotlib.pyplot as plt
import matplotlib.ticker as mticker
import seaborn as sns
sns.set()
import params


def plot_setup_ax(ax, plot_range, xticks, yticks, alpha, plot_topo=False): 
    """Create map background for plotting spatial data"""

    ax.set_extent(plot_range, crs=ccrs.PlateCarree())
    ax.coastlines(linewidth=mpl.rcParams["contour.linewidth"])

    gl = ax.gridlines(
        draw_labels=True,
        linestyle="--",
        alpha=alpha,
        linewidth=params.plot_params["gridline_width"],
        color="k",
        zorder=1.05,
    )
    gl.top_labels = False
    gl.right_labels = False
    gl.xlabel_style = {"size": mpl.rcParams["xtick.labelsize"]}
    gl.ylabel_style = {"size": mpl.rcParams["ytick.labelsize"]}
    gl.ylocator = mticker.FixedLocator(yticks)
    gl.xlocator = mticker.FixedLocator(xticks)

    if plot_topo:
        # load topography map
        topo = xr.open_dataset("topo.nc")
        topo = topo["bath"].sel(X=slice(230, 300), Y=slice(15, 52))

        ## Plot 1000m contour of topography
        ax.contour(
            topo.X,
            topo.Y,
            topo,
            extend="both",
            colors="k",
            levels=[-10000, 1000],
            transform=ccrs.PlateCarree(),
            linewidths=mpl.rcParams["contour.linewidth"]/2,
        )

    return ax, gl


if __name__=="__main__":

    params.set_plot_style(scale=1.)

    fig = plt.figure(figsize=(3,2), layout="constrained")
    ax = fig.add_subplot(projection=ccrs.PlateCarree(central_longitude=180)) 

    ## setup background for the plot
    ax, gl = plot_setup_ax(
        ax,
        plot_range=[235, 290, 15, 52],
        xticks=[-120, -105, -90, -75],
        yticks=[20, 30, 40, 50],
        alpha=0.1,
        plot_topo=True,
    )
    fig.savefig("map.png")
