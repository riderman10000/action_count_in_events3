import os 
import logging
import numpy as np 
import pandas as pd 
import statsmodels.api as sm 
from sklearn.decomposition import PCA, IncrementalPCA

logging.basicConfig(
    format="{asctime} - {levelname} - {message}",
    style="{",
    datefmt="%Y-%m-%d %H:%M",
    level= logging.DEBUG,
)

def pca_smoothing(data: np.ndarray):
    logging.debug(f"data shape: {data.shape}")
    ipca = IncrementalPCA(n_components=1, batch_size=10) 
    ipca_data = ipca.fit_transform(data)
    ipca_data = np.reshape(ipca_data, -1)
    _, smooth = sm.tsa.filters.hpfilter(ipca_data) 
    logging.debug(f"ipca data shape: {ipca_data}")
    return smooth
    ...