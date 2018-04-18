# Main text figures

## Figure 1

```bash
python2.7 plot_risk_measure_individual.py \
    --filetype=.png \
    --country=uk \
    --outfilename=fig_1 \
    --weeks 1 2 3 4 5 28
```

![./graphics/fig_1.png](./graphics/fig_1.png)

**Fig 1. Instantaneous risk of onward transmission of foot-and-mouth disease in UK 2001 in first 5 weeks and the final week**  Calculated as the infectious pressure from an average-sized infectious farm to an average-sized susceptible farm integrated across both the joint parameter distribution at the time point in question, and from 0 to 20km.  Note that the instantaneous risk of transmission indicates the overall relative risk of transmission, which does not have a direct epidemiological interpretation but provides a direct comparison across weeks.  

## Figure 2

```bash
python2.7 plot_three_panel_plot.py \
    --filetype=.png \
    --country=uk \
    --outfilename=fig_2 \
    --randomseed=100 \
    --weeks 1 2 3 4 5 28
```

![./graphics/fig_2.png](./graphics/fig_2.png)

**Fig 2. Projections and relative rankings of various control strategies of total animals culled, and estimates of infected but undetected farms, for the first five weeks and the final week of the 2001 foot-and-mouth disease outbreak in UK.**  A) Distribution of total animal culls from forward simulations, here shown as kernel density estimates (violin plots), are seeded either using parameter estimates from the end of the outbreak (‘complete’), or at the specific time point (‘accrued’).  B) Rankings of control interventions are according to median projections.  Proportion (C) of times each control was optimal when bootstrap samples are made from distributions in (A).  For all time points see figs S9 and S10.  

## Figure 3

```bash
python2.7 plot_three_panel_plot.py \
    --filetype=.png \
    --country=japan \
    --outfilename=fig_3 \
    --randomseed=100 \
    --weeks 1 2 3 4 5 11
```

**Fig 3. Projections and relative rankings of various control strategies of total animals culled, and estimates of infected but undetected farms, for the first five weeks and final week of the 2010 foot-and-mouth disease outbreak in Miyazaki, Japan.**  A) Distribution of total animal culls from forward simulations, here shown as kernel density estimates (violin plots), are seeded either using parameter estimates from the end of the outbreak (‘complete’), or at the specific time point (‘accrued’).  B) Rankings of control interventions are according to median projections.  Proportion (C) of times each control was optimal when bootstrap samples are made from distributions in (A).  For all time points see fig S11.  


--- 

# Supporting Information figures


## Figure S1, S2

We can't share data for figures S1 and S2 (so code is omitted for them).  

#### Figure S3

```bash
python2.7 plot_params_mean_95CI.py \
    -f=.png \
    -w 1 2 3 4 5 6 7 8 9 10 11 \
    --figw=9.5 --figh=7 \
    --outputfilename=fig_s3 \
    --ncols=4 --nrows=4

$convert -density 300 \
    ./graphics/fig_s3.pdf \
    -resize 2200 \
    -depth 8 \
    -compress lzw \
    -flatten ./graphics/figure_s3.tif
```

![./graphics/fig_s3.png](./graphics/fig_s3.png)


## Figure S4


```bash
python2.7 plot_risk_measure_individual.py \
    --filetype=.png \
    --country=japan \
    --outfilename=fig_s4 \
    --weeks 1 2 3 4 5 11

```

![./graphics/fig_s4.png](./graphics/fig_s4.png)

## Figure S5

## Figure S6

## Figure S7

## Figure S8

## Figure S9 - adjust the height/width of the output plot in `plot_three_panel_plot.py`

## Figure S10 - adjust the height/width of the output plot in `plot_three_panel_plot.py`

## Figure S11 - adjust the height/width of the output plot in `plot_three_panel_plot.py`

```bash
python2.7 plot_three_panel_plot.py \
    --filetype=.pdf \
    --country=japan \
    --outfilename=figure_s11 \
    --randomseed=100 \
    --weeks 1 2 3 4 5 6 7 8 9 10 11
```

