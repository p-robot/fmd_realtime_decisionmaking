# Script to generate figures for "Real-time decision-making during emergency disease outbreaks"
# 
# Data, downloaded as Supplementary Information, is assumed to be in the `data` folder.  
# Run scripts from the main project folder, `fmd_realtime_decisionmaking`.  That is:
# 
# cd fmd_realtime_decisionmaking
# ./run.sh
# 
# W. Probert, 2018

# Clean/process the parameter data from raw data files
#python clean_params_uk.py
#python clean_params_japan_hdf5.py

# Clean/process the simulation data from raw data files
#python clean_simulation_output_uk.py
#python clean_simulation_output_japan.py


# Generate figures

# Figure 1
echo "Generating figure 1"
python plot_risk_measure_individual.py \
    --filetype=.png \
    --country=uk \
    --outfilename=fig_1 \
    --weeks 1 2 3 4 5 28


# Figure 2
echo "Generating figure 2"
python plot_three_panel_plot.py \
    --filetype=.png \
    --country=uk \
    --outfilename=fig_2 \
    --randomseed=100 \
    --weeks 1 2 3 4 5 28


# Figure 3
echo "Generating figure 3"
python plot_three_panel_plot.py \
    --filetype=.png \
    --country=japan \
    --outfilename=fig_3 \
    --randomseed=100 \
    --weeks 1 2 3 4 5 11


# S3
echo "Generating figure S3"
python plot_params_mean_95CI.py \
    -f=.png \
    -w 1 2 3 4 5 6 7 8 9 10 11 \
    --figw=9.5 --figh=7 \
    --outputfilename=fig_s3 \
    --ncols=4 --nrows=4


# S4
echo "Generating figure S4"
python plot_risk_measure_individual.py \
    --filetype=.png \
    --country=japan \
    --outfilename=fig_s4 \
    --weeks 1 2 3 4 5 11


# S5
echo "Generating figure S5"
python plot_scatterplot_params.py \
    -p1=psi_1 -p2=gamma_1 \
    -w 1 2 3 4 5 6 \
    -c=uk \
    -f=".png"\
    --outfilename="fig_s5"

# S6
echo "Generating figure S6"
python plot_scatterplot_params.py \
    -p1=phi_2 -p2=zeta_2 \
    -w 1 2 3 4 5 6 \
    -c=japan \
    -f=".png" \
    --outfilename="fig_s6"


# # Figure s7 and s8
# python ~/Projects/temporal_model_fitting/temporal_model_fitting/plot_map_county_occult_scatter.py \
#     --c=uk --f=.png --o=fig_s7


# python ~/Projects/temporal_model_fitting/temporal_model_fitting/plot_map_county_occult_scatter.py --c=japan --f=.png --o=fig_s8


# S9
echo "Generating figure S9"
python plot_three_panel_plot.py \
    --filetype=.png \
    --country=uk \
    --outfilename=fig_s9 \
    --randomseed=100 \
    --figw=14 \
    --figh=7 \
    --sim_legend=True \
    --legend_size=8 \
    --accrued_xtext=Ac \
    --complete_xtext=Co \
    --weeks 1 2 3 4 5 6 7 8 9 10 11 12

# S10
echo "Generating figure S10"
python plot_three_panel_plot.py \
    --filetype=.png \
    --country=uk \
    --outfilename=fig_s10 \
    --randomseed=100 \
    --figw=14 \
    --figh=7 \
    --sim_legend=True \
    --legend_size=8 \
    --accrued_xtext=Ac \
    --complete_xtext=Co \
    --weeks 13 14 15 16 17 18 19 20 21 22 23 24 25 26 27 28

# S11
echo "Generating figure S11"
python plot_three_panel_plot.py \
    --filetype=.png \
    --country=japan \
    --outfilename=fig_s11 \
    --randomseed=100 \
    --figw=14 \
    --figh=7 \
    --sim_legend=True \
    --legend_size=8 \
    --accrued_xtext=Ac \
    --complete_xtext=Co \
    --weeks 1 2 3 4 5 6 7 8 9 10 11
