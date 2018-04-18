"""
Calculate a measure of risk of onward spread for an average-sized farm to an 
average-sized farm, integrated across a range of distances.  

"""

import pandas as pd, numpy as np, argparse
from os.path import join
from matplotlib import pyplot as plt

def susceptibility(row, japan = False):
    """
    Farm-level susceptibility
    """
    
    if japan:
        v = 1**row.psi_1 + row.xi_2*1**row.psi_2
    else:
        v = 1**row.psi_1 + row.xi_2*1**row.psi_2 + row.xi_3*1**row.psi_3
    
    return v


def transmissibility(row, japan = False):
    """
    Farm-level transmissibility
    """
    
    if japan:
        v = 1**row.phi_1 + row.zeta_2*1**row.phi_2
    else:
        v = 1**row.phi_1 + row.zeta_2*1**row.phi_2 + row.zeta_3*1**row.phi_3
    
    return v


def K(Dsq, delta, omega):
    """
    Kernel function
    """
    return delta/(delta**2 + Dsq)**omega


if __name__=="__main__":
    
    alpha = 0.6
    
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
    
    # Load parameter and demography data
    if args.country == "japan":
        
        infile_params = 'cleaned_params_japan_vaccine_standard16.7.20.csv'
        
        colour = "#e31a1c"
        rgba = [0.89, 0.102, 0.11, alpha]
        
        weeks = np.asarray(args.weeks);
        times = (weeks - 1)*7 + 34
        
        ylims = np.arange(-6, 8, step = 2)
    else:
        infile_params = 'cleaned_params_uk.csv'
        
        colour = "#1f78b4"
        rgba = [0.122, 0.471, 0.706, alpha]
        
        weeks = np.asarray(args.weeks);
        times = (weeks - 1)*7 + 26
        
        ylims = range(-2, 3)
    
    df_params = pd.read_csv(join('.', 'data', infile_params))
    
    risks = []
    # For each time step
    for t in times:
    
        # Subset the dataset
        if args.country == "japan":
            sub = df_params[(df_params.day == t)]
        else:
            sub = df_params[(df_params.day == t) & (df_params.rep <= 2000)]
        
        # For each point in the posterior distribution (occults are disregarded)
        suscept = susceptibility(sub, (args.country == "japan"))
        
        # Calculate susceptibility and transmissibility
        transmiss = transmissibility(sub, (args.country == "japan"))
        
        # Calculate full kernel
        output = []
        Dsq = np.linspace(0, 500, 100)
        for d in Dsq:
            o = sub.gamma1 * suscept * transmiss * K(d, sub.delta, sub.omega)
            #o = o * sub.gamma2 + sub.epsilon1*sub.epsilon2
            
            output.append(o.values)
    
        output = np.array(output).T
        risk = output.sum(axis = 1)
        risks.append(risk)


    r = [np.log10(rr) for rr in risks]
    fig, ax = plt.subplots()
    N = len(r)
    violins = ax.violinplot(r, points = 40, widths = [0.7]*N, showmeans = False, \
        showextrema = True, showmedians = True)

    for b in violins['bodies']:
        b.set_facecolor(rgba)#"#FF530D")#9ecae1
        b.set_edgecolor(colour)#"#E82C0C")#3182bd
        b.set_linewidth(1.0)

    #cmeans = violins['cmeans']
    #cmeans.set_color("#1F2ECC")

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

    ax.spines['top'].set_visible(False)
    ax.spines['right'].set_visible(False)
    ax.xaxis.set_ticks_position('bottom')
    ax.yaxis.set_ticks_position('left')

    ax.set_xlabel("Week since first confirmed case")
    ax.set_ylabel("Risk of onward transmission (log$_{10}$)")
    
    ax.set_xticks(np.arange(len(weeks))+1)
    ax.set_xticklabels(weeks)

    ax.set_yticks(ylims)
    ax.set_yticklabels(ylims)

    fig.set_size_inches(9, 5)
    plt.savefig(join('.', 'graphics', args.outfilename + args.filetype))
    plt.close()

