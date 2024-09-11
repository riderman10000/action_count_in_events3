import os 
import logging
import numpy as np 
import matplotlib.pyplot as plt 
import pandas as pd 

logging.basicConfig(
    format="{asctime} - {levelname} - {message}",
    style="{",
    datefmt="%Y-%m-%d %H:%M",
    level= logging.DEBUG,
)


class_num = 2 
file_names = os.listdir("./event_csv/split_data/class2/")
file_name = file_names[0] # select the file to read and analyze

file_path = f"./event_csv/split_data/class{class_num}/{file_name}"
logging.debug(file_path) # f'../../event_csv/split_data/class{class_num}/{file_name}')
data_df = pd.read_csv(file_path, dtype=np.int8)
logging.debug(data_df)
logging.debug(data_df.describe())

# event data processing
after_manhattan =  {
    
}

count = 0 
x1, y1, x2, y2 = 0
for index, row in enumerate(data_df.iterrows()):
    x1, y1 = row[1], row[2]
    if index == 0:
        x2, y2 = data_df['x'][index + 1], data_df['y'][index + 1]
    
    # manhattan distance 
    delta_x, delta_y = abs(x2 - x1), abs(y2 - y1)
    delta = 5 # distance between x1 and x2, or y1 and y2  
    
    # getting a good starting point and checking if the data is noise or not
    if not (delta_x <= delta and delta_y <= delta):
        # checking if we reached the end 
        if index + 1 >= data_df.shape[0]:
            if count > 1 : 
                ...
            break 
        
        if count == 1:
            continue
        
        continue