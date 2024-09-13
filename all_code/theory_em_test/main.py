import os 
import logging
import numpy as np 
import matplotlib.pyplot as plt 
import pandas as pd 
import statsmodels.api as sm 

# custom python file 
import test_pca

logging.basicConfig(
    format="{asctime} - {levelname} - {message}",
    style="{",
    datefmt="%Y-%m-%d %H:%M",
    level= logging.DEBUG,
)
# set font 
from pylab import mpl 
mpl.rcParams['font.sans-serif'] = ["SimHei"]
# solve the problem of negative sign display 
plt.rcParams['axes.unicode_minus'] = False 
# set the width of the coordinate axis 
plt.rcParams['axes.linewidth'] = 2

class_num = 2 
file_names = os.listdir("./event_csv/split_data/class2/")
file_name = file_names[0] # select the file to read and analyze

file_path = f"./event_csv/split_data/class{class_num}/{file_name}"
logging.debug(file_path) # f'../../event_csv/split_data/class{class_num}/{file_name}')
data_df = pd.read_csv(file_path, dtype=np.int8)
logging.debug(data_df)
logging.debug(data_df.describe())

# event data processing

count = 0 
counter = 1
count_margin = 100
x1, y1, x2, y2 = 0, 0, 0, 0
manhattan_chunk = np.zeros((count_margin, 2), dtype=np.uint8)
temp_pca_data = np.array([])

for index, row in enumerate(data_df.iterrows()):
    if index == 0 :
        x1, y1 = data_df['x'][index], data_df['y'][index] # row[1]['x'], row[1]['y']
        manhattan_chunk[0][0], manhattan_chunk[0][1] = x1, y1 
        continue
    
    if (counter % count_margin) == 0:
        temp_pca_data = np.concatenate([temp_pca_data, test_pca.pca_smoothing(manhattan_chunk)])
        counter = 0
        first = False
            # plt.plot(temp_pca_data) 
            # plt.show() 
        ...
    
    x2, y2 = data_df['x'][index], data_df['y'][index]

    # manhattan distance 
    delta_x, delta_y = abs(x2 - x1), abs(y2 - y1)
    delta = 5 # distance between x1 and x2, or y1 and y2  
    
    # getting a good starting point and checking if the data is noise or not
    is_not_noise = (delta_x <= delta and delta_y <= delta)
    in_count_margin = (count < count_margin) 
    
    if is_not_noise and in_count_margin:
        count += 1 
        manhattan_chunk[counter][0], manhattan_chunk[counter][1] = x2, y2 
        counter += 1 
        # continue
    else:
        # checking if we reached the end 
        if index + 1 >= data_df.shape[0]:
            if count > 1 : 
                # write to the remaining data less than the count margin
                # call your function 
                # pca_smoothing 
                _, smooth = sm.tsa.filters.hpfilter(temp_pca_data)
                smooth_df = pd.DataFrame(smooth)
                smooth_df.plot()
                ...
            break
        x3, y3  = data_df['x'][index+1], data_df['y'][index+1]
        delta_x, delta_y = abs(x3 - x2), abs(y3 - y2)
        is_noise = (delta_x > delta and delta_y > delta)
        if count == 1 and  is_noise:
            continue

        manhattan_chunk[counter] = np.array([x2, y2])
        counter += 1 
        
        x1, y1 = x2, y2 
        count = 1 
    # logging.debug(f"[*] count: {count} @ {counter}, x1: {x1}, y1: {y1} | x2: {x2}, y2: {y2}")
_, smooth = sm.tsa.filters.hpfilter(temp_pca_data)
smooth_df = pd.DataFrame(smooth)
smooth_df.plot()
plt.show()