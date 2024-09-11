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
file_names = os.listdir("../../event_csv/split_data/class2/")
file_name = file_names[0] # select the file to read and analyze
logging.debug(f'../../event_csv/split_data/class{class_num}/{file_name}')

file_path = f'../../event_csv/split_data/class{class_num}/{file_name}'
data_df = pd.read_csv(file_path, dtype=np.int8)
logging.debug(data_df)
logging.debug(data_df.describe())
