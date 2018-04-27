#!/usr/bin/python
"""
Generate three-panel plots of simulation output, ranking of interventions, and proportion of times
each intervention was optimal.  

Usage:

python plot_three_panel_plot.py <country> [--filetype <filetype>] [--outfilename=<outfile>] [--weeks 1 2 3 ...]

This script assumes the input data for UK is within the file
"cleaned_temp_model_fit_sim_runs_reruns.csv" and the input data for Miyazaki in the file
"cleaned_temp_model_fit_sim_runs_japan_Aug2016.csv".  These are stored within the folders
"./data/japan" for Miyazaki, and "./data" for the UK data.  


Parameters
----------
--country : str ("japan" or "uk")
    
--filetype : str (default .eps)
    Graphics filetype for the output figure, to be passed to matplotlib's pyplot.savefig() function

--outfilename : str
    Output filename (default filename concatenates other information)

--weeks : space delimited list of ints (i.e. "1 2 3")
    The "weeks since outbreak started" to use for plotting

--figw : width of the output figure

--figh : height of the output figure


W. Probert, 2015
"""

import sys, os, argparse
from os.path import join
import numpy as np, pandas as pd
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
from matplotlib.ticker import ScalarFormatter

from colours import *

# Turn off the pandas SettingWithCopyWarning.  
pd.options.mode.chained_assignment = None


if __name__ == "__main__":
    
    # Process the input argument
    parser = argparse.ArgumentParser()
    
    parser.add_argument("-c", "--country", type = str, required = True,
        help = "Country of interest ('uk' or 'japan')")
    
    parser.add_argument('-w','--weeks', nargs = '+', required = True, type = int)
    
    parser.add_argument("--filetype", type = str, 
        help = "Filetype to be used for the output plots", default = ".eps")
    
    parser.add_argument("--outfilename", type = str, 
        help = "Output filename (excluding the filetype suffix)", default = None)
        
    parser.add_argument("--sim_legend", type = bool, 
        help = "Should a legend be plotted for the simulation output", default = True)
    
    parser.add_argument("--legend_size", type = int, 
        help = "Size of the legend", default = 9)
    
    parser.add_argument("--accrued_xtext", type = str, 
        help = "Text on x-axis to denote columns of accrued information", default = "Accr.")
    
    parser.add_argument("--complete_xtext", type = str, 
        help = "Text on x-axis to denote columns of complete information", default = "Comp.")
    
    parser.add_argument('--figw', type = float, default = 48/5.5, 
        help = "Figure output width")
    
    parser.add_argument('--figh', type = float, default = 30/5.5, 
        help = "Figure output height")
    
    args = parser.parse_args()
    
    sys.stdout.write("Generating plots for: " + args.country + "\n")
    sys.stdout.write("Generating plots with filetype: " + args.filetype + "\n")
    sys.stdout.write("Plotting a legend for the simulation output: " + str(args.sim_legend) + "\n")
    sys.stdout.write("Plotting weeks: " + " ".join(str(x) for x in args.weeks)  + "\n")
    
    weeks = np.asarray(args.weeks); T = len(args.weeks)
    
    # Functions for summarising simulation output and then generating rankings of interventions
    # can use alternative functions - see commented code below.  
    functions = [np.mean] #lambda x: np.percentile(x, 95)], np.median,np.var,()]
    function_names = ['mean']#, 'median', 'var', 'q95']95 perc
    
    variables = ["total_culls"]
    vars_texts = ['Total culls (head)']
    
    # Import the data
    full = pd.read_csv(join('.', 'data', 'simulation_output_' + args.country + '.csv'))
    counts_full = pd.read_csv(join('.', 'data', 'counts_' + args.country + '.csv'))
    
    # UK-specific parameters
    if args.country == "uk":
        outbreak_start = pd.datetime(year = 2001, month = 2, day = 19)
        
        ctrl_order = ['ip', 'ipdc', 'ipdccp', 'rc3', 'rc10', 'v3', 'v10']
        ctrl_names = ctrl_order
    
    # Miyazaki-specific parameters
    elif args.country == "japan":
        outbreak_start = pd.datetime(year = 2010, month = 4, day = 20)
        
        ctrl_order = ['ip', 'ipdc', 'rc3', 'rc10', 'v3', 'v10']
        ctrl_names = ctrl_order
    
    # Calculate number of interventions
    n = len(ctrl_order)
    
    skip_weeks = [17, 18, 19, 21, 22, 23, 25, 26, 27]
    weeks_to_plot = np.setdiff1d(weeks, skip_weeks)
    
    # List for storing the rankings.  
    rankings = []
    
    for i_p, var, ylabel in zip(range(len(variables)), variables, vars_texts):
        
        # To change the relative sizing of subplots... 
        nrows = 15; ncols = T
        
        fig = plt.figure() 
        
        # Set up a numpy array of axes objects with the desired row/col spans
        axes = []
        for i in [0, 9, 12]:
            axs = []
            for j in range(ncols):
                if i == 0:
                    ax = plt.subplot2grid((nrows,ncols),(i, j), rowspan = 9)
                elif i == 9:
                    ax = plt.subplot2grid((nrows,ncols),(i, j), rowspan = 3)
                elif i == 12:
                    ax = plt.subplot2grid((nrows,ncols),(i, j), rowspan = 3)
                
                axs.append(ax)
            axes.append(axs)
        axes = np.array(axes)
        
        for i_v, params in enumerate(['current', 'final']):
            
            # Subset the data based on the type of parameters used
            # (this is used later for calculating limits of axes)
            x = full.loc[full.params_used == params][var]
            
            subset = full.loc[full.params_used == params]
            subset = subset.loc[subset.control.isin(ctrl_order)]
            
            subset['date'] = outbreak_start + pd.to_timedelta(full.week, unit = 'W')
            
            # Within each param set, and within each week, calc rank of ctrls
            cols_of_int = ['params_used', 'date', 'control']
            sub = subset.groupby(cols_of_int)[var].agg(functions)
            sub.columns = function_names
            sub.reset_index(inplace = True)
            
            sub_long = pd.melt(sub, id_vars = ['date', 'control'], value_vars = function_names)
            
            sub_long['ranking'] = sub_long.groupby(['variable', 'date'])['value'].rank(
                ascending = False, method = 'min', na_option = 'keep')
            
            # Ensure the ranking of the controls is consistent with their order
            cat_control = pd.Categorical(sub_long['control'], \
                categories = ctrl_order, ordered = True)
            
            sub_long['control'] = cat_control
            
            sub_long = sub_long.sort_values(by = ['date', 'control'], ascending = [1, 1])
            
            for ii, t in enumerate(weeks):
                
                # Axes of interest
                ax_i = ii
                
                axes[0, ax_i].axhline(0, color = colour_line, linewidth = 3.0)
                axes[1, ax_i].axhline(0, color = colour_line, linewidth = 3.0)
                axes[2, ax_i].axhline(0, color = colour_line, linewidth = 3.0)
                
                # At each point in time, do the following:
                #   - plot the points of rankings
                #   - find the previous index, and the next index (within times_to_..)
                
                # Using np.float for conversion here cause of ongoing issue with pd.to_timedelta
                # see here: https://github.com/pandas-dev/pandas/issues/8757
                date_curr = outbreak_start + pd.to_timedelta(np.float(t), unit = 'W')
                rank_curr = sub_long.loc[sub_long['date'] == date_curr]
                
                if t not in skip_weeks:
                    # Plot circles at each forward simulation point.  
                    rankings.append(rank_curr.ranking.values)
                    
                    for i_cc, cc in enumerate(ctrl_order):
                        
                        axes[1,ax_i].plot(-0.5 + i_v, \
                            rank_curr.loc[rank_curr.control == cc].ranking.values,\
                            label = cc.upper(), color = colour_dict_controls[cc]['chex'], \
                            linewidth = 0.5, marker = 'o', ms = 6, \
                            markeredgewidth = 0.0, \
                            markeredgecolor = 'grey') 
                
                axes[1,ax_i].set_xlim([-1, 1])
                axes[1,ax_i].set_ylim([0, n + 1])
                
                axes[1, ax_i].set_frame_on(False)
                axes[1, ax_i].xaxis.set_ticks_position('bottom')
                axes[1, ax_i].yaxis.set_ticks_position('left')
                axes[1, ax_i].set_xticks([])
                axes[1, ax_i].set_xticklabels([])
                
                if t in skip_weeks:
                    pass
                else:
                    sys.stdout.write("week " + str(t) + "\n")
                    
                    cond1 = (full.params_used == params)
                    cond2 = (full.week == t)
                    dt = full.loc[cond1 & cond2]
                    
                    data = [dt.loc[dt.control == ctrl][var] for ctrl in ctrl_order]
                    
                    # For controls side by side:
                    #pos = np.linspace(1, n, n)*2 + (i_v - 1)
                    
                    # For accrued/complete side by side:
                    gap = 2
                    pos = np.linspace(1, n, n) + i_v*n + i_v*gap
                    
                    boxes = axes[0, ax_i].violinplot(data, pos, \
                        points = 50, widths = [0.7]*n, showmeans = True, \
                        showextrema = True, showmedians = True)
                    
                    for b, cc in zip(boxes['bodies'], ctrl_order):
                        b.set_facecolor(colour_dict_controls[cc]['crgba'])
                        b.set_edgecolor(colour_dict_controls[cc]['chex'])
                        b.set_linewidth(0.1)
                        b.set_alpha(0.8)
                    
                    means = boxes['cmeans']
                    means.set_color(colour_line)
                    means.set_alpha(1.0)
                    means.set_linestyle('-')
                    means.set_linewidth(2.0)
                    
                    bars = boxes['cbars']
                    bars.set_linewidth(0.25)
                    bars.set_color('grey')
                    bars.set_alpha(0.9)
                    
                    maxes = boxes['cmaxes']
                    maxes.set_color('grey')
                    maxes.set_alpha(0.9)
                    maxes.set_linewidth(0.25)
                    
                    mins = boxes['cmins']
                    mins.set_color('grey')
                    mins.set_alpha(0.9)
                    mins.set_linewidth(0.25)
                    
                    medians = boxes['cmedians']
                    medians.set_color('grey')
                    medians.set_alpha(0.0)
                    medians.set_linewidth(2.0)
                    
                axes[0, ax_i].set_frame_on(False)
                axes[0, ax_i].set_xticks([])
                axes[0, ax_i].set_xticklabels([])
                
                for mid_ax in np.arange(T, T):
                    axes[0, mid_ax].set_frame_on(False)
                    axes[0, mid_ax].set_xticks([])
                    axes[0, mid_ax].set_xticklabels([])
                    axes[0, mid_ax].set_yticks([])
                    axes[0, mid_ax].set_yticklabels([])
                    
                    axes[1, mid_ax].set_frame_on(False)
                    axes[1, mid_ax].set_xticks([])
                    axes[1, mid_ax].set_xticklabels([])
                    axes[1, mid_ax].set_yticks([])
                    axes[1, mid_ax].set_yticklabels([])
                    
                if (ax_i == 0):
                    axes[0, ax_i].yaxis.set_ticks_position('left')
                    axes[1, ax_i].yaxis.set_ticks_position('left')
                    for tick in axes[i_v, 0].yaxis.get_major_ticks():
                        tick.label.set_fontsize(10) # 24
                else:
                    axes[0, ax_i].yaxis.set_visible(False)
                    axes[1, ax_i].yaxis.set_visible(False)
                
                xlim = [-1, 2*n+gap+2]
                axes[0, ax_i].set_xlim(xlim)
                
                if args.country == "japan":
                    if (var == 'total_culls'):
                        limits = [0, full[var].max()*1.1]
                else:
                    if (var == 'total_culls'):
                        limits = [0, x.max() + 0.2*10E6]
                    limits = [0, full[var].max()]
                
                if (var == "total_culls"):
                    formatter = ScalarFormatter()
                    formatter.set_powerlimits((1,4))
                    axes[i_v, 0].yaxis.set_major_formatter(formatter)
                    axes[i_v, 0].yaxis.offsetText.set_fontsize(8)
                
                axes[0, ax_i].set_ylim(limits)
                
                if t in skip_weeks:
                    pass
                else:
                    # Plot the stochastic output
                    c1 = (counts_full.week == t)
                    c2 = (counts_full.objective == var)
                    c3 = (counts_full.params_used == params)
                    sub = counts_full.loc[c1&c2&c3]
                    
                    sub['colors'] = sub.control.map(colour_dict_controls_hex)
                    
                    sub['control'] = pd.Categorical(sub['control'], ctrl_order)
                    sub = sub.sort_values(by = 'control')
                    
                    tot = sub.counts.sum()
                    
                    cumsums = sub.counts.cumsum(skipna = True)/tot
                    bottoms = [0]
                    to_add = list(cumsums[0:(n - 1)])
                    bottoms.extend(to_add)
                    
                    # Calculate the left-hand-side anchor for stacked bars
                    width = 0.25
                    ctr_offset = 0.5
                    ctr = 1
                    
                    left = (ctr - ctr_offset) + ctr_offset*2*i_v - width/2.
                    
                    ba = axes[2, ax_i].bar([left]*(n), \
                        height = sub.counts/tot, bottom = bottoms, \
                        color = sub.colors, alpha = 0.7, \
                        width = width, linewidth = 0)
                
                axes[2, ax_i].set_frame_on(False)
                axes[2, ax_i].xaxis.set_ticks_position('bottom')
                axes[2, ax_i].yaxis.set_ticks_position('left')
                axes[2, ax_i].set_yticklabels([])
                axes[2, ax_i].set_yticks([])
                axes[2,ax_i].set_xlim([0, 2])
                
                # PLOTTING THE 'A' and 'C' for accrued and complete
                axes[2, ax_i].set_xticks([ctr - ctr_offset, ctr + ctr_offset])
                
                if t in skip_weeks:
                    axes[2, ax_i].set_xticks([])
                    axes[2, ax_i].set_xticklabels([])
                else:
                    axes[2, ax_i].set_xticks([ctr - ctr_offset, ctr + ctr_offset])
                    axes[2, ax_i].set_xticklabels([args.accrued_xtext, args.complete_xtext])
            
                for tick in axes[2, ax_i].xaxis.get_major_ticks():
                    tick.label.set_fontsize(8) # 26
            
                # Add horizontal lines to designate changes in time step
                # don't put a line on the first or last panels.  
                if (t > 0) & (t != weeks[-1]):
                    axes[0, ax_i].axvline(axes[0, ax_i].get_xlim()[1], \
                        color = colour_faint_line, linewidth = 1.0, ymin = 0.05)
                    axes[1, ax_i].axvline(axes[1, ax_i].get_xlim()[1], \
                        color = colour_faint_line, linewidth = 1.0, ymin = 0.1)
                    axes[2, ax_i].axvline(axes[2, ax_i].get_xlim()[1], \
                        color = colour_faint_line, linewidth = 1.0, ymin = 0.1)
                
                # Tick labels on bottom axis
                if t in skip_weeks:
                    axes[2, ax_i].set_xlabel("")
                else:
                    axes[2, ax_i].set_xlabel(str(t), size = 12, weight = 'bold')
            
            # Set the ticks and labels on the ranking plots
            axes[1,0].set_yticks(np.arange(n) + 1)
            axes[1,0].set_yticklabels(np.flipud(np.arange(n) + 1))
            
            for tick in axes[1,0].yaxis.get_major_ticks():
                tick.label.set_fontsize(8)
            
            # Set the ticks and labels on the stochastic analysis plots
            axes[2,0].set_yticks(np.linspace(0, 1, 2))
            axes[2,0].set_yticklabels(np.linspace(0, 1, 2))
            
            for tick in axes[2,0].yaxis.get_major_ticks():
                tick.label.set_fontsize(8)
                
            # Turn off the ticks on the right hand side of the plot
            axes[i_v, i_v].yaxis.set_ticks_position('left')
        
        if args.sim_legend:
            ax0 = 0
            ax1 = T - 1
            
            # Add custom legend to the final subplot
            handles = []
            for c, lab in zip(ctrl_order, ctrl_names):
                patch = mpatches.Patch(color = colour_dict_controls[c]['chex'], \
                    alpha = alpha_control, label = lab.upper())
                handles.append(patch)
            
            plt.sca(axes[ax0, ax1])
            legend_all = plt.legend(handles = handles, bbox_to_anchor = (1.1, 1.1), \
                numpoints = 1, frameon = False, prop = {'size': args.legend_size})
            
            axes[ax0, ax1].add_artist(legend_all)
        
        # Add subplot labels to the figure
        line_props = {'fontsize': 18, 'weight': 'bold'} # 36
        
        plt.figtext(0.01, 0.94, 'A', **line_props)
        plt.figtext(0.01, 0.44, 'B', **line_props)
        plt.figtext(0.01, 0.24, 'C', **line_props)
        
        # Add figure text for the simulation parameters
        label_props = {'size': 12, 'weight': 'bold', 'va': 'center', 'ha': 'center'}
        sub_props = {'size': 10, 'weight': 'normal'}
        
        vertical_props = {'rotation': 90, 'va': 'center', 'ha': 'center'}
        
        # Add main label to the y-axis on the RHS
        plt.figtext(0.047, 0.7, ylabel, size = 10, weight = 'bold', **vertical_props)
        plt.figtext(0.047, 0.38, "Ranking", size = 9, weight = 'bold', **vertical_props)
        
        plt.figtext(0.049, 0.21, "Prop. times", size = 8, **vertical_props)
        plt.figtext(0.06, 0.21, "optimal", size = 8, **vertical_props)
        
        y_label = "Weeks since first confirmed case"
        plt.figtext(0.5, 0.03, y_label, weight = 'bold', \
            va = 'center', ha = 'center', size = 14)
        
        # Turn off the tick marks for the bottom tick in the top two panels
        for ax in [0,1]:
            yticks = axes[ax,0].yaxis.get_ticklines()
            yticks[0].set_markeredgewidth(0.0)
            yticks[-1].set_markeredgewidth(0.0)
        
        axes[0, 0].axvline(axes[0, 0].get_xlim()[0], \
            color = colour_line, linewidth = 3.0)
        
        ax10_lim = axes[1, 0].get_xlim()[0]
        axes[1,0].axvline(ax10_lim, color = colour_line, linewidth = 3.0)
        axes[2,0].axvline(0, color = colour_line, linewidth = 3.0)
        
        fig.subplots_adjust(left = 0.09, bottom = 0.14, \
            right = 0.985, top = 0.95, wspace=0.0, hspace=0.35)
        
        fig.set_size_inches(args.figw, args.figh)
        
        # Determine the output filename
        if args.outfilename is None:
            filename = '_'.join(['FIG', "T"+str(T), var, params, args.country])
        else:
            filename = args.outfilename
        
        plt.savefig(join('.', 'graphics', filename + args.filetype), dpi = 600)
        plt.close()
