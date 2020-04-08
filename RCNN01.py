import numpy as np # linear algebra
import pandas as pd # data processing, CSV file I/O (e.g. pd.read_csv)
from glob import glob
import os
from skimage.io import imread
import matplotlib.pyplot as plt
import seaborn as sns
# %matplotlib inline
dsb_data_dir = os.path.join('..', 'input')
stage_label = 'stage1'