"""
Correlation plots between the empirical marginal posterior distributions of two parameters

Parameters that are plotted on the log scale are gamma1, epsilon1, epsilon2.  Parameters that are plotted with y-axis of [0,1] are phi_1 phi_2 psi_1 psi_2.  Otherwise, the limits for the
y-axis are taken as the limits for the parameter in question across all weeks (including those
that are not plotted).  

Usage:
plot_scatterplot_parameters.py --param1=<parameter1> --param2<parameter2> --weeks 1 2 3 4 5 --filetype=<.eps> --outfilename=<output_filename>


Parameters
----------
param1 : str
    Parameter 1 of interest (x axis)

param2 : str
    Parameter 2 of interest (y axis)

weeks : list of int
    Weeks to plot

country : str ("japan" or "uk")
    Country from which to draw data

outfilename : str
    File name to use for output filetype
"""

import sys, os, argparse
from os.path import join
import numpy as np, pandas as pd
import matplotlib.pyplot as plt

# Import plotting default colours and styles.  
from colours import *

def rounddown(x, dp = 2):
    return np.floor(x*(10**dp))/10**dp

def roundup(x, dp = 2):
    return np.ceil(x*(10**dp))/10**dp

as_zero_to_one = ['phi_1', 'phi_2', 'psi_1', 'psi_2']
as_logged = ['gamma1', 'epsilon1', 'epsilon2'] #'e1e2'

# Use 3 ticks for both axes
NTICKS = 3

if __name__ == "__main__":
    
    # Process the input argument
    parser = argparse.ArgumentParser()
    
    parser.add_argument("--param1", "-p1", type = str, required = True,
        help = "Parameter 1 of interest (xaxis)")
    
    parser.add_argument("--param2", "-p2", type = str, required = True,
        help = "Parameter 2 of interest (xaxis)")
    
    parser.add_argument('-w','--weeks', nargs = '+', required = True, type = int)
    
    parser.add_argument("-c", "--country", type = str, required = True,
        help = "Country of interest ('uk' or 'japan')")
    
    parser.add_argument("-f", "--filetype", type = str, 
        help = "Filetype to be used for the output plots", default = ".eps")
    
    parser.add_argument("-o", "--outfilename", type = str, 
        help = "Output filename (excluding the filetype suffix)", default = None)
    
    args = parser.parse_args()
    
    # Import the data
    if args.country == "uk":
        
        full = pd.read_csv(join('.', 'data', 'parameters_uk.csv'))
        
        # 'Week 1' in the UK data started on the 19th Feb 2001
        full['week'] = (full.day - 19)/7.
        
    elif args.country == "japan":
        
        full = pd.read_csv(join('.', 'data', 'parameters_japan.csv'))
        
        # 'Week 1' in the Miyazaki data started on the 27th April 2010
        full['week'] = (full.day - 27)/7.
    
    full['e1e2'] = full.epsilon1 * full.epsilon2
    
    weeks = np.array(args.weeks)
    T = len(weeks)
    
    if args.param1 in as_logged:
        full[args.param1] = np.log(full[args.param1])
    
    if args.param2 in as_logged:
        full[args.param2] = np.log(full[args.param2])
    
    param1_lims = [rounddown(full[args.param1].min()), 
                    roundup(full[args.param1].max())]
    param2_lims = [rounddown(full[args.param2].min()), 
                    roundup(full[args.param2].max())]
    
    print("param1_lims", param1_lims)
    print("param2_lims", param2_lims)
    
    if args.param1 in as_zero_to_one:
        param1_lims = [0, 1]
    if args.param2 in as_zero_to_one:
        param2_lims = [0, 1]
    
    fig, ax = plt.subplots(ncols = T, nrows = 1)
    
    for axi, t in enumerate(weeks):
        
        # Subset the dataset to the week in question
        subset = full[full.week == t]
        
        ax[axi].scatter(subset[args.param1], subset[args.param2], 
            s = 3, lw = 0, c = colour_dict_country[args.country]["crgba"])
        
        ax[axi].set_xlim(param1_lims)
        ax[axi].set_ylim(param2_lims)
        
        if axi > 0:
            ax[axi].set_xticks([])
            ax[axi].set_xticklabels([])
            ax[axi].set_yticks([])
            ax[axi].set_yticklabels([])
        else:
            ax[axi].set_xticks(np.linspace(param1_lims[0], param1_lims[1], NTICKS))
            ax[axi].set_yticks(np.linspace(param2_lims[0], param2_lims[1], NTICKS))
        
        #ax[axi].set_frame_on(False)
        # ax[axi].axhline(param1_lims[0], color = colour_line, linewidth = 3.0)
        # ax[axi].axvline(param2_lims[0], color = colour_line, linewidth = 3.0)
        
        ax[axi].spines['top'].set_visible(False)
        ax[axi].spines['right'].set_visible(False)
        
        ax[axi].tick_params(labelsize = 8, length = 0.0)
        
        # Can plot week number using xlabel as follows:
        #ax[axi].set_xlabel('\n\n'+str(t), fontsize = 12)
        ax[axi].text(0.5, -0.15, str(t), size = 12, ha = "center", transform = ax[axi].transAxes)
    
    if args.param1 in as_logged:
        ax[0].set_xlabel('log $\\' + args.param1 + '$', fontsize = 14)
    else:
        ax[0].set_xlabel('$\\' + args.param1 + '$', fontsize = 14)
        
    if args.param2 in as_logged:
        ax[0].set_ylabel('log $\\' + args.param2 + '$', fontsize = 14)
    else:
        ax[0].set_ylabel('$\\' + args.param2 + '$', fontsize = 14)
    
    plt.figtext(0.53, 0.02, 'Week since first confirmed case', \
        va = 'center', ha = 'center', **text_props)
    
    if args.outfilename:
        filename = args.outfilename
    else:
        filename = "_".join([args.param1, args.param2, args.country])
    
    # Set the maximum size of the figure for the journal
    fig.set_size_inches((9.5, 7))
    
    fig.subplots_adjust(left = 0.09, bottom = 0.2, \
        right = 0.985, top = 0.95, wspace=0.05, hspace=0.0)
    
    plt.savefig(join('.', 'graphics', filename + args.filetype))
    plt.close()
