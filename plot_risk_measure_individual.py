"""
Calculate and plot the instantaneous risk of onward spread for an average-sized farm to an 
average-sized farm, integrated across a range of distances.  

Usage 

python plot_risk_measure_individual.py <country> [--filetype <filetype>] [--outfilename=<outfile>] [--randomseed=<seed>] [--weeks 1 2 3 ...]

"""

import pandas as pd, numpy as np, argparse
from os.path import join
from matplotlib import pyplot as plt

from colours import *


def susceptibility(row, japan = False):
    """
    Calculate farm-level susceptibility for an average-sized susceptible farm.  
    
    Parameters
    ----------
    row : object
        Object with attributes psi_1, psi_2, xi_2 for Japan and additional xi_3, psi_3 for UK.
    japan : boolean
        Should this calculation be for the Miyazaki model?  
    
    Returns
    -------
    Float 
        Farm-level susceptibility
    """
    
    if japan:
        v = 1**row.psi_1 + row.xi_2*1**row.psi_2
    else:
        v = 1**row.psi_1 + row.xi_2*1**row.psi_2 + row.xi_3*1**row.psi_3
    
    return v


def transmissibility(row, japan = False):
    """
    Calculate farm-level transmissibility
    
    Parameters
    ----------
    row : object
        Object with attributes phi_1, phi_2, zeta_2 for Japan and additional zeta_3, phi_3 for UK.
    japan : boolean
        Should this calculation be for the Miyazaki model?  
    
    Returns
    -------
    Float 
        Farm-level transmissibility
    """
    
    if japan:
        v = 1**row.phi_1 + row.zeta_2*1**row.phi_2
    else:
        v = 1**row.phi_1 + row.zeta_2*1**row.phi_2 + row.zeta_3*1**row.phi_3
    
    return v


def K(Dsq, delta, omega = 1.3):
    """
    Evaluate the distance kernel function
    
    Parameters
    ----------
    Dsq : float
        Squared-distance at which to evaluate the kernel
    
    delta, omega : floats
        Parameters of the distance kernel (see Methods appendix of the manuscript for details)
    
    Returns
    -------
    Float
        Distance kernel with parameters `delta` and `omega` evaluated at squared-distance `Dsq`
    
    """
    return delta/(delta**2 + Dsq)**omega


if __name__=="__main__":
    
    # Process the input argument
    parser = argparse.ArgumentParser()
    
    parser.add_argument("-c", "--country", type = str, required = True,
        help = "Country of interest ('uk' or 'japan')")
    
    parser.add_argument('-w','--weeks', nargs = '+', required = True, type = int)
    
    parser.add_argument("--filetype", type = str, 
        help = "Filetype to be used for the output plots", default = ".eps")
    
    parser.add_argument("--outfilename", type = str, 
        help = "Output filename (excluding the filetype suffix)", default = None)
    
    args = parser.parse_args()
    
    colour = colour_dict_country[args.country]['chex']
    
    # Load parameter and demography data
    if args.country == "japan":
        
        rgba = [0.89, 0.102, 0.11, alpha_country]
        
        weeks = np.asarray(args.weeks);
        times = (weeks - 1)*7 + 34
        
        ylims = np.arange(-6, 8, step = 2)
    else:
        
        rgba = [0.122, 0.471, 0.706, alpha_country]
        
        weeks = np.asarray(args.weeks);
        times = (weeks - 1)*7 + 26
        
        ylims = range(-2, 3)
    
    infile_params = 'parameters_' + args.country + '.csv'
    df_params = pd.read_csv(join('.', 'data', infile_params))
    
    # List container to store risk measures for each week of interest
    risks = []
    
    # For each time step
    for w in weeks:
    
        # Subset the dataset
        sub = df_params[(df_params.week == w)]
        
        # For each point in the posterior distribution (occults are disregarded)
        suscept = susceptibility(sub, (args.country == "japan"))
        
        # Calculate susceptibility and transmissibility
        transmiss = transmissibility(sub, (args.country == "japan"))
        
        # Calculate full kernel
        output = []
        Dsq = np.linspace(0, 500, 100)
        
        for d in Dsq:
            o = sub.gamma_1 * suscept * transmiss * K(d, sub.delta)
            output.append(o.values)
        
        output = np.array(output).T
        risk = output.sum(axis = 1)
        risks.append(risk)
    
    # Take log10 of the instantaneous risks
    r = [np.log10(rr) for rr in risks]
    N = len(r)
    
    fig, ax = plt.subplots()
    
    violins = ax.violinplot(r, \
        points = 40, widths = [0.7] * N, \
        showmeans = False, \
        showextrema = True, showmedians = True)
    
    # Adjust colors of faces/medians/outliers/whiskers of the violin plots
    for b in violins['bodies']:
        b.set_facecolor(rgba)
        b.set_edgecolor(colour)
        b.set_linewidth(1.0)
    
    cmedians = violins['cmedians']
    cmedians.set_color("#1F2ECC")
    
    cbar = violins['cbars']
    cbar.set_color('grey')#e34a33
    
    mx = violins['cmaxes']
    mx.set_color('#666666')
    mx.set_alpha(0.5)
    mx.set_linewidth(1.5)
    
    mn = violins['cmins']
    mn.set_color('#666666')
    mn.set_alpha(0.5)
    mn.set_linewidth(1.5)
    
    # Adjust box surrounding the plot
    ax.spines['top'].set_visible(False)
    ax.spines['right'].set_visible(False)
    ax.xaxis.set_ticks_position('bottom')
    ax.yaxis.set_ticks_position('left')
    
    # Set axis labels
    ax.set_xlabel("Week since first confirmed case")
    ax.set_ylabel("Risk of onward transmission (log$_{10}$)")
    
    # Set x-axis tick positions and tick labels
    ax.set_xticks(np.arange(len(weeks))+1)
    ax.set_xticklabels(weeks)
    
    # Set y-axis tick positions and tick labels
    ax.set_yticks(ylims)
    ax.set_yticklabels(ylims)
    
    # Adjust figure size (w, h)
    fig.set_size_inches(7, 4)
    
    # Trim the edges of the plot
    fig.subplots_adjust(left = 0.1, bottom = 0.15, \
        right = 0.95, top = 0.95, wspace = 0.0, hspace = 0.0)
    # Save figure and close figure object
    plt.savefig(join('.', 'graphics', args.outfilename + args.filetype), dpi = 300)
    plt.close()
