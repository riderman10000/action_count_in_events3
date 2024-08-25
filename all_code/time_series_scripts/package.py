import os
import cv2
import matplotlib.pyplot as plt
from matplotlib.font_manager import FontProperties
import numpy as np
import pandas as pd
import scipy.spatial.distance as dist
from scipy.stats import kurtosis, skew
from pylab import mpl 
import pymannkendall as mk
import statsmodels.api as sm
from fastdtw import fastdtw
from sklearn.decomposition import PCA
# Set font
mpl.rcParams["font.sans-serif"] = ["SimHei"]
# Solve the problem of negative sign display
plt.rcParams['axes.unicode_minus'] = False
# Set the width of the coordinate axis
plt.rcParams['axes.linewidth'] = 2