""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""
 Utilities to plot OISST data
    1) ex_plot_func     : example plotting function to use in make_gif function
    2) make_gif         : generates figures from plotting fucntion, makes GIF, and saves GIF
    
""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""

# import necessary packages and functions for plotting
import os,imageio
import matplotlib.pyplot as plt
import matplotlib.ticker as mticker
import matplotlib.dates as dates
import matplotlib.colors as colors 
import cartopy
import calendar
import cartopy.crs as ccrs
from os import path
from mpl_toolkits.axes_grid1 import make_axes_locatable
from mpl_toolkits.axes_grid1.inset_locator import inset_axes
from cartopy.mpl.gridliner import LONGITUDE_FORMATTER, LATITUDE_FORMATTER
import matplotlib.patches as patches
import seaborn as sns

# turn off warnings
import warnings
warnings.filterwarnings("ignore")

# import the data util functions
# from utils.exampleFolder_data_utils import *


#--------------------------------------------------------------------------------------------------------------------------------- # 1) returns a figure of the daily SST anomalies in the northwest Atlantic

def ex_plot_func(sst_file, bathy_file, day, year, fig_quality, setCol, setCol_min, setCol_max):
    """""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""
    Input: 
        sst_file (xarray)      : SST file of daily anomalies in the northwest Atlantic, e.g. OISST data
        bathy_file (xarray)    : bathy of the northwest Atlantic
        day (Int)              : day of the year (0-365)
        year (Int)             : year of interest (e.g. 2016)
        fig_quality (Int)      : quality of the figure (e.g. 100 dpi) 
        setCol (Bool)          : True to manually set colorbar limits, False to use default min, max 
        setCol_min (Int)       : minimum value for colormap of SST anomalies
        setCol_max (Int)       : maximum value for colormap of SST anomalies
    
    Output:
        fig (Figure)           : returns figure of plot of SST anomalies in the northwest Atlantic for that given day
     
    """""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""
    
    # define bonds for northwest Atlantic region
    x_bnds = [-77,-48] # lon
    y_bnds = [35,53] # lat
    
    proj = ccrs.PlateCarree()
    
    # create figure with axes
    fig,ax = plt.subplots(subplot_kw = dict(projection=proj))
    
    # set colormap limits
    if setCol: 
        sst_min = setCol_min # set lower limit of colorbar
        sst_max = setCol_max # set uppper limit of colorbar
    elif not setCol:
        sst_min, sst_max = find_minMax_daily(sst_file) 
        # find_mixMax_daily() is a function I made to return the min and max temp for all SSTAs in a given year 
    
    # plot
    im = (sst_file[day]).plot(add_colorbar=False, levels=np.linspace(sst_min, sst_max, 2000))
    
    # get month
    month = int(sst_file.time[day].dt.month.values)
    
    # axes formatting
    ax.set_title(str(calendar.month_name[month])+' '+str(year)) # changes title of figure for each month
    ax.set_xlabel('Longitude')
    ax.set_ylabel('Latitude')
    ax.contour(bathy_file.lon,bathy_file.lat,bathy_file.z,levels=[-4000,-1000,-100],colors='gray') # 100, 1000, 4000-m isobaths
    ax.coastlines(resolution='50m',color='gray')
    ax.set_extent([x_bnds[0],x_bnds[1],y_bnds[0],y_bnds[1]], crs=ccrs.PlateCarree())
    ax.add_feature(cartopy.feature.LAND, color='lightgray')
    ax.plot(get_gs_month(year,month-1)[0],get_gs_month(year,month-1)[1], color='k')
    # get_gs_month returns the GS path for a given year and month
    
    # gridlines
    gl = ax.gridlines(crs=proj,draw_labels=True)
    gl.xlabels_top = False
    gl.ylabels_right = False
    gl.yformatter = LATITUDE_FORMATTER
    gl.xformatter = LONGITUDE_FORMATTER

    return fig


#---------------------------------------------------------------------------------------------------------------------------------
# 2) creates a GIF and saves it to specified path
def make_gif(sst_file, bathy_file, year, setCol, setCol_min, setCol_max, image_duration, figure_path, gif_path, gif_name):
    """""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""
    Input:
        sst_file (xarray)       : daily SST anomalies for the given year
        bathy_file (xarray)     : bathy file for northwest Atlantic
        year (Int)              : year of interest (e.g. 2016)
        setCol (Bool)           : True to manually set colorbar limits, False to use default min, max 
        setCol_min (Int)        : minimum value for colorbar
        setCol_max (Int)        : maximum value for colorbar
        image_duration (Int)    : how long each image in the gif displays for
        figure_path (Str)       : path for saving figures, e.g. 'vortexfs1/home/eperez/ssf/OISST/animationPlots'
        gif_path (Str)          : path for saving the gif, e.g. '/vortexfs1/home/eperez/ssf/OISST/'
        gif_name (Str)          : name of gif, e.g. 'sst_anom2016'
    
    Output:
        * no output, saves GIF
     
    """""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""

    # plot all figures needed for gif and save to a folder specifically for these figures
    for i in range(366):
        plot_anom_daily(nwa_anom_daily,bathy,i,year,100,setCol, setCol_min,setCol_max).savefig(figure_path+str(i)+'.png',bbox_inches='tight');

    images,image_file_names = [],[]
    for file_name in os.listdir('figure_path'):
        if file_name.endswith('.png'):
            image_file_names.append(file_name)       
    sorted_files = sorted(image_file_names,key=lambda x: int(os.path.splitext(x)[0]))

    for filename in sorted_files:
        images.append(imageio.imread(figure_path+filename))
    imageio.mimsave(gif_path+gif_name+'.gif', images,duration=image_duration) # e.g. image_duration = 0.08
    

#---------------------------------------------------------------------------------------------------------------------------------
    
    
    
    