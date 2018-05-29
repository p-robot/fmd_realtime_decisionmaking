"""


--randomseed : int  (default 100)
    Random seed for the bootstrap test

"""

import sys, argparse
from os.path import join
import numpy as np, pandas as pd

if __name__ == "__main__":
    
    
    # Process the input argument
    parser = argparse.ArgumentParser()
    
    parser.add_argument("-c", "--country", type = str, required = True,
        help = "Country of interest ('uk' or 'japan')")
    
    parser.add_argument("--randomseed", type = int, 
        help = "Random seed for initialising bootstrap sampling", default = 100)
    
    parser.add_argument("--nboot", type = int, 
        help = "Number of bootstrap samples", default = 1000)
    
    args = parser.parse_args()
    
    # Define the parameters for the bootstrapping
    
    np.random.seed(args.randomseed)
    
    if args.country == "uk":
        ctrl_order = ['ip', 'ipdc', 'ipdccp', 'rc3', 'rc10', 'v3', 'v10']
    else: 
        ctrl_order = ['ip', 'ipdc', 'rc3', 'rc10', 'v3', 'v10']
    
    # Calculate number of interventions
    n = len(ctrl_order)
    
    # Import the dataset
    full = pd.read_csv(join('.', 'data', 'simulation_output_' + args.country + '.csv'))
    
    for ip, par in enumerate(['final', 'accrued']):
        sys.stdout.write("Generating boostrap samples from " + par + " parameters\n")
        
        # Subset the dataset to the parameter set and control 
        full_all = full.loc[(full.params_used == par) & (full.control.isin(ctrl_order))]
        
        for iv, var in enumerate(['total_culls']):
            
            model_results = []
            
            for w in full_all.week.unique():
                optimal = []
                sub = full_all.loc[full_all.week == w]
                
                n_controls = len(sub.control.unique())
                if n_controls != n:
                     sys.stdout.write("Not same number of controls in the data as expected\n")
                
                n_runs = sub.shape[0]/n_controls
                
                shifts = (np.arange(n_controls)*n_runs).astype(int)
                
                sub = sub.reset_index()
                sub = sub.sort_values(by = 'control')
                
                for i in range(args.nboot):
                    # Draw 5 random numbers (for each of the control actions)
                    # between 0 and n_runs
                    row = np.random.randint(n_runs, size = n_controls)
                    
                    # Add the starting row numbers.  
                    comparison_df = sub.iloc[row + shifts]
                    
                    # Find the minimum
                    imin = comparison_df[var].idxmin() # idxmin; argmin
                    
                    opt_df = comparison_df.loc[imin,:]
                    
                    if comparison_df.shape[0] != n:
                        sys.stdout.write("Number of controls in the data not as expected")
                    
                    # there may be ties... so this may be a list
                    if isinstance(opt_df.control, str):
                        optimal.append(opt_df.control)
                    else:
                        optimal.extend(list(opt_df.control))
                    
                counts = pd.Categorical(optimal, categories = ctrl_order).value_counts()
                
                model_results.append(optimal)
                
                if (w == 1) & (par == 'final'):
                    counts_full = pd.DataFrame(counts)
                    counts_full = counts_full.reset_index()
                    counts_full.columns = ['control', 'counts']
                    counts_full['week'] = w
                    counts_full['objective'] = var
                    counts_full['params_used'] = par
                else:
                    counts = pd.DataFrame(counts)
                    counts = counts.reset_index()
                    counts.columns = ['control', 'counts']
                    counts['week'] = w
                    counts['objective'] = var
                    counts['params_used'] = par
                    
                    counts_full = pd.concat([counts_full, counts])
    
    cols2keep = ['week', 'params_used', 'control', 'counts']
    counts_full[cols2keep].to_csv(join('.', 'data', 'counts_' + args.country + '.csv'), 
        index = False)
