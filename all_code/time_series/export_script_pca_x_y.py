# from time_series_scripts import data_compress
import sys
import os 

import pandas as pd 
import numpy as np 

import yaml 

import statsmodels.api as sm 

sys.path.append('../') # going a step back so the importer can find the following module
from time_series_scripts import data_compress_data as dcd
from time_series_scripts import data_compress as dc 
from time_series_scripts import cycle_count as cc 

# name = "user02_lab.csv" # - 13
# name = "user02_fluorescent.csv" # - 15
# name = "user02_fluorescent_led.csv" # - 13
# name = "user02_led.csv" # - python - 12 - esp 17
# name = "user02_natural.csv" # - python - 12 - esp 15 
class_num = 3
name = "user02_fluorescent.csv" # - python - 12 - esp 15 
# file_path = f'../../event_csv/compress_event_manhattan/class{class_num}/smooth_by_pca/compress_by_mean/{name}'
file_path = f'../../event_csv/split_data/class{class_num}/{name}'


for class_num in [4, 5, 6, 7]: # classes 
    for name in [       # names of files 
        "user02_lab.csv",
        "user02_fluorescent.csv",
        "user02_fluorescent_led.csv",
        "user02_led.csv",
        "user02_natural.csv",
    ]:
        os.makedirs(f"./figs/class{class_num}/", exist_ok=True)
        file_path = f'../../event_csv/split_data/class{class_num}/{name}'
        file_stream = open(f"./figs/class{class_num}/{name.split('.')[0] + '.yaml'}", 'w' )    
        info = {}   
        # reading the csv file 
        df = pd.read_csv(file_path)
        # filtering data with manhattan
        manhattan_df = dcd.compress_by_Manhattan(df) 

        # dimensionality_reduction_PCA 
        pca_df = dcd.dimensionality_reduction_PCA(manhattan_df)

        # for x and y 
        _, smooth_x = sm.tsa.filters.hpfilter(manhattan_df['x']) 
        _, smooth_y = sm.tsa.filters.hpfilter(manhattan_df['y']) 

        smooth_x = smooth_x-smooth_x.mean()
        smooth_y = smooth_y -smooth_y.mean()


        # mean compression for the pca 
        pca_mean_df = dcd.compress_by_mean(pca_df)

        # mean compression for each signal x and y 
        mean_x_df = dcd.compress_by_mean(pd.DataFrame(smooth_x))
        mean_y_df = dcd.compress_by_mean(pd.DataFrame(smooth_y))

        import matplotlib.pyplot as plt

        fig, axs = plt.subplots(3, figsize=(12, 8))  # Width: 10 inches, Height: 6 inches


        fig.suptitle(f"file path = {file_path} \nplot of class: {class_num}, file_name: {name}")

        plot_names  = ["PCA", "only x", "only  y"]
        for index, data_df in enumerate([pca_mean_df['value'], mean_x_df['value'], mean_y_df['value']]):
            win_change,top_win,win_size,step = cc.get_index_of_bottom_and_top_by_mk(data_df)
            
            axs[index].plot(data_df)
            current = 0 
            start = 0 
            for i , (win, trend) in enumerate(zip(win_change, top_win)):
                if i == 0:
                    start = win
                    current = trend
                    continue
                axs[index].plot(data_df[start: win], color='red' if current else 'blue')
                start = win 
                current = trend 
            print(
                "count from python ", 
                cc.get_dtw_mean_cost(win_change, top_win, data_df))
            current_counts = cc.get_dtw_mean_cost(win_change, top_win, data_df)
            axs[index].set_title(f"Plot of {plot_names[index]}")
            axs[index].text(0, data_df.min(), f"std: {data_df.std():.2f} || action count: {current_counts}")

            info[plot_names[index]] =  {
                'std' : float(data_df.std()),
                'count': current_counts,
            }
            
        yaml.safe_dump(info, file_stream)
        file_stream.close()
            
        # axs[3].plot([a for a in range(len(data_df))])

        # plt.text(1.5, 0, "Important Information")
        plt.tight_layout()
        # Save the plot
        plt.savefig(f"./figs/class{class_num}/{name.split('.')[0] + '.png'}")