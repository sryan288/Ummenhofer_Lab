## Plotting parameters
plot_params = {
    "gridline_width":0.7,
    "border_width":0.3,
    "tick_width":0.0,
    "tick_length":2.,
    "twocol_width":5.5,
    "onecol_width":3.2,
    "max_width":6.4,
}

def set_plot_style(scale=1.):
    """Set plot style.
    'scale' controls size of figures and fonts"""

    import matplotlib as mpl
    import seaborn as sns
    sns.set()
    sns.set_palette("colorblind")
    
    ## Manually change some parameters 
    # mpl.rcParams["text.usetex"]       = True
    # mpl.rcParams["font.family"]       = "Computer Modern Roman"
    mpl.rcParams['figure.dpi']        = 300 # set figure resolution (dots per inch) 
    mpl.rcParams['hatch.linewidth']   = .15  * scale
    mpl.rcParams['axes.labelsize']    = 9  * scale
    mpl.rcParams['axes.titlesize']    = 11  * scale
    mpl.rcParams['xtick.labelsize']   = 9   * scale
    mpl.rcParams['ytick.labelsize']   = 9   * scale
    mpl.rcParams['font.size']         = 9   * scale
    mpl.rcParams['lines.linewidth']   = 1   * scale
    mpl.rcParams['legend.fontsize']   = 8   * scale
    mpl.rcParams['legend.title_fontsize']   = 8   * scale
    mpl.rcParams['patch.linewidth']   = 1   * scale
    mpl.rcParams['contour.linewidth'] =.5   * scale
    mpl.rcParams['axes.labelpad']     = 4 * scale   # space between label and axis
    mpl.rcParams['xtick.major.pad']   = 0 * scale   # distance to major tick label in points
    mpl.rcParams['ytick.major.pad']   = mpl.rcParams['xtick.major.pad']
    mpl.rcParams['lines.markersize']  = 3 * scale

    return

