# Import required libraries
import tensorflow as tf
from tensorflow import keras
from tensorflow.keras.preprocessing import image_dataset_from_directory
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from PIL import Image, ImageDraw
from skimage import color
from skimage.transform import resize
import gdown
import os
import glob
import random
from sklearn.model_selection import train_test_split
import math
from tensorflow.keras.preprocessing import image_dataset_from_directory
from keras.layers import Conv2D, Conv2DTranspose, Input, Dropout, MaxPool2D, concatenate, Activation, \
  BatchNormalization, GlobalAvgPool2D, Flatten, Reshape, Dense
from keras.models import Model, Sequential, load_model
from tensorflow.keras.applications import *

# Import custom functions
import functions

# Setting value
AUTOTUNE = tf.data.AUTOTUNE
img_size = 150
n_train = 6500
n_val = 7106 - 6500
LR = 0.0001
n_batch = 32
n_epoch = 100

# Write directory address
cur_dir = os.getcwd()
data_dir = os.path.join(cur_dir, "landscape_data")
x_dir = os.path.join(data_dir, "gray")
y_dir = os.path.join(data_dir, "color")

# Checking amount of data > 7129 / 7129
x_image_files = [fname for fname in os.listdir(x_dir) if os.path.splitext(fname)[-1]=='.jpg']
len(x_image_files)
y_image_files = [fname for fname in os.listdir(y_dir) if os.path.splitext(fname)[-1]=='.jpg']
len(y_image_files)

# Remove Images of different size
for path in x_image_files:
  temp = np.array(Image.open(os.path.join(x_dir, path))).shape
  if temp != (img_size, img_size):
    os.remove(os.path.join(x_dir, path))
  else:
    continue

# Update gray data list and check amount
x_image_files = [fname for fname in os.listdir(x_dir) if os.path.splitext(fname)[-1]=='.jpg']
len(x_image_files)

# Contrast the datasets of color and gray images to prevent datasets are different situation
for path in y_image_files:
  if path not in x_image_files:
    os.remove(os.path.join(y_dir, path))
  else:
    continue

# Update color data list and check amount
y_image_files = [fname for fname in os.listdir(y_dir) if os.path.splitext(fname)[-1]=='.jpg']
len(y_image_files)

# Additionally, reconfirm that there are files with different image sizes in the color datasets
for path in y_image_files:
  temp = np.array(Image.open(os.path.join(y_dir, path))).shape
  if temp != (img_size, img_size, 3):
    print(path)
  else:
    continue

# Load data
x = np.array([np.array(Image.open(os.path.join(x_dir, image))) for image in x_image_files])
# To match with the shape of the color datasets, adjust shape of gray datasets
x = x.reshape(-1, img_size, img_size, 1)
y = np.array([np.array(Image.open(os.path.join(y_dir, image))) for image in y_image_files])
print(f"x_shape / y_shape : {x.shape, y.shape}")

# Data scailing between 0 and 1
x, y = x/x.max(), y/y.max()
print(x.shape, x.max(), x.min(), y.shape, y.max(),y.min())

# Split train dataset and validation dataset
train_x, val_x, train_y, val_y = train_test_split(x, y, test_size = 0.1, shuffle = True, random_state = 32)