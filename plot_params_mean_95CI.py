"""
Plotting function for parameter values in the temporal model fitting analysis

This script plots the parameter values for a given number of weeks (since the first confirmed 
case) for both UK and Miyazaki outbreaks.  For each week the mean parameter value and the 2.5
and 97.5 percent quantiles are plotted for both countries.  Japan is plotted in red and UK is 
plotted in blue.  

Usage: 
plot_params_mean_95CI.py --filetype=<filetype> --weeks <weeks>

filetype : str
    File type for output figure, as passed to plt.savefig.  

weeks : list of int
    Weeks of data to plot
"""

# Set latex-related parameters for rending the axes titles (ignored if generating a png file)
# import matplotlib
# matplotlib.rcParams['font.family'] = 'serif'
# matplotlib.rcParams['font.serif'] = 'cm'

import sys, os, argparse
import pandas as pd, numpy as np, sys
from os.path import join
from matplotlib import pyplot as plt
import matplotlib.patches as mpatches

from colours import *

# Functions to use for plotting
def quant025(x):
    return(x.quantile(0.025))

def quant975(x):
    return(x.quantile(0.975))

functions = [np.mean, quant025, quant975]
function_names = ['avg', 'L95', 'U95']

# Parameters to plot on the log scale
as_logged = ['gamma_1', 'epsilon_1', 'epsilon_2']

# Parameters to plot with 0 - 1 limits
as_zero_to_one = ['phi_1', 'phi_2', 'psi_1', 'psi_2']


if __name__ == "__main__":
    
    # Process the input argument
    parser = argparse.ArgumentParser()
    
    parser.add_argument("-f", "--filetype", type = str, 
        help = "Filetype to be used for the output plots", default = ".eps")
    
    parser.add_argument("--outputfilename", type = str, 
        help = "File name to be used for the output plots", default = "output")
    
    parser.add_argument('-w','--weeks', nargs = '+', type = int, required = True)
    
    parser.add_argument('--figw', type = float, default = 9.5)
    parser.add_argument('--figh', type = float, default = 7.0)
    
    parser.add_argument('--nrows', type = int, default = 4)
    parser.add_argument('--ncols', type = int, default = 4)
    
    args = parser.parse_args()
    
    fulluk = pd.read_csv(join('.', 'data', 'parameters_uk.csv'))
    fullj = pd.read_csv(join('.', 'data', 'parameters_japan.csv'))
    
    # 'Week 1' in the UK data started on the 19th Feb 2001
    # 'Week 1' in the Miyazaki data started on the 27th April 2010
    #fullj['week'] = (fullj.day - 27)/7.
    #fulluk['week'] = (fulluk.day - 19)/7.
    
    all_columns = np.union1d(fullj.columns, fulluk.columns)
    columns_to_plot = ['delta', 'epsilon_1', 'epsilon_2', 'gamma_1', 'gamma_2', 'phi_1', 'phi_2', \
        'phi_3', 'psi_1', 'psi_2', 'psi_3', 'xi_2', 'xi_3', 'zeta_2', 'zeta_3']
    
    times = np.array(args.weeks)
    
    fig, axes = plt.subplots(ncols = args.ncols, nrows = args.nrows, frameon = False)
    fig.subplots_adjust(wspace = 0.3, hspace = 0.3, bottom = 0.1, top = 0.9, left = 0.05, right = 0.95)
    
    sys.stdout.write("Plotting variable: ")
    for ivar, var in enumerate(columns_to_plot):
        
        axx = int(np.mod(ivar, args.ncols))
        axy = int(ivar // args.ncols)
        
        sys.stdout.write(var + ", ")
        
        if var in fullj.columns:
            if var in as_logged:
                fullj[var] = np.log(fullj[var])
            jmin = fullj[var].quantile(0.005)
            jmax = fullj[var].quantile(0.995)
        
        if var in fulluk.columns:
            if var in as_logged:
                fulluk[var] = np.log(fulluk[var])
            ukmin = fulluk[var].quantile(0.005)
            ukmax = fulluk[var].quantile(0.995)
        
        ymin = np.min([ukmin, jmin])
        ymax = np.max([ukmax, jmax])
        
        # Calculate the mean, 2.5-th, and 97.5-th quantile.  
        
        for icountry, df in enumerate([fulluk, fullj]):
            if var in df.columns:
                if icountry == 0:
                    linestyle_avg = {'linestyle': "-", 
                        'c': colour_dict_country['uk']['chex']}
                        
                    linestyle_ci = {'linestyle': "--", \
                        'c': colour_dict_country['uk']['crgba']}
                else:
                    linestyle_avg = {'linestyle': "-", \
                        'c': colour_dict_country['japan']['chex']}
                    linestyle_ci = {'linestyle': "--", \
                        'c': colour_dict_country['japan']['crgba']}
                
                subdf = df[df.week.isin(times)]
                
                grouper = subdf.groupby('week').agg({var: functions}).reset_index()
                
                grouper.columns = ['week'] + function_names
                
                axes[axy, axx].plot(grouper.week.values, grouper.avg.values, **linestyle_avg)
                
                axes[axy, axx].fill_between(grouper.week.values, 
                    grouper.L95.values, grouper.U95.values, 
                    where =  grouper.L95.values <= grouper.U95.values,
                    facecolor = linestyle_ci['c'], interpolate = True, lw = 0.0)
        
        axes[axy, axx].set_xticks([])
        axes[axy, axx].set_xticklabels([])
        
        axes[axy, axx].tick_params(labelsize = 8, length = 0.0)
        
        axes[axy, axx].set_frame_on(False)
        axes[axy, axx].set_title('$\\' + var + '$', fontsize = 12)
        
        axes[axy, axx].axvline(times.min() - 0.25, color = '#2b2b2b', linewidth = 1.0)
        axes[axy, axx].set_xlim([times.min() - 0.25, times.max()])
        
        if var in as_zero_to_one:
            axes[axy, axx].set_ylim([0, 1])
            axes[axy, axx].axhline(0, color = '#2b2b2b', linewidth = 1.0)
        else:
            axes[axy, axx].set_ylim([ymin, ymax])
            axes[axy, axx].axhline(ymin, color = '#2b2b2b', linewidth = 1.0)
        
        if (axy == (args.nrows - 1)) | ((axx == (args.ncols - 1)) & (axy == (args.nrows -2))):
            axes[axy, axx].set_xticks(times)
            axes[axy, axx].set_xticklabels(times, fontsize = 8)
            axes[axy, axx].yaxis.set_ticks_position('left')
            axes[axy, axx].xaxis.set_ticks_position('bottom')
            axes[axy, axx].tick_params(labelsize = 8, length = 0.0)
    
    sys.stdout.write("\n")
    
    plt.figtext(0.53, 0.03, 'Week since first confirmed case', \
        va = 'center', ha = 'center', **text_props)
    
    axes[3, 3].axis('off')
    
    fig.set_size_inches((args.figw, args.figh))
    
    plt.savefig(join(".", "graphics", args.outputfilename + args.filetype), dpi = 300)
    plt.close()
