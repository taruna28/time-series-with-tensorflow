# -*- coding: utf-8 -*-
"""Untitled8.ipynb

Automatically generated by Colaboratory.

Original file is located at
    https://colab.research.google.com/drive/1O-7qOtPpVj6LprbsCWEYBsJak5uxKYdX

time series maxtemp australia
"""

import numpy as np
import pandas as pd
from keras.layers import Dense, LSTM
import matplotlib.pyplot as plt
import tensorflow as tf

data_train = pd.read_csv('weatherAUS.csv')
data_train.head()

data_train.isnull().sum()

data_train['Date']=pd.to_datetime(data_train['Date'])
data_train['Date'].head()
data_train['MaxTemp'].fillna(data_train['MaxTemp'].mean(), inplace=True) # we will fill the null row
df = data_train[['Date','MaxTemp']]
df.head()

df.info()

# df['date'] = pd.to_datetime(df['date'])
 
# #df.sort_values(by='date')
# df.head()

# dates = data_train['Date'].values
# temp  = data_train['MaxTemp'].values
# #  salah
 
# plt.figure(figsize=(15,5))
# plt.plot(dates, temp)
# plt.title('Temperature average',
#           fontsize=20);

aus=df[['Date','MaxTemp']].copy()
aus['date'] = aus['Date'].dt.date

ausfinal=aus.drop('Date',axis=1)
ausfinal.set_index('date', inplace= True)
ausfinal.head()

plt.figure(figsize=(20,8))
plt.plot(ausfinal)
plt.title(' Weather')
plt.xlabel('Date')
plt.ylabel('MaxTemp')
plt.show()

# get data values
date = data_train['Date'].values
temp = data_train['MaxTemp'].values

def windowed_dataset(series, window_size, batch_size, shuffle_buffer):
    series = tf.expand_dims(series, axis=-1)
    ds = tf.data.Dataset.from_tensor_slices(series)
    ds = ds.window(window_size + 1, shift=1, drop_remainder=True)
    ds = ds.flat_map(lambda w: w.batch(window_size + 1))
    ds = ds.shuffle(shuffle_buffer)
    ds = ds.map(lambda w: (w[:-1], w[-1:]))
    return ds.batch(batch_size).prefetch(1)

from sklearn.model_selection import train_test_split

x_train, x_test, y_train, y_test = train_test_split(temp, date, test_size = 0.2, random_state = 0 , shuffle=False)
print(len(x_train), len(x_test))

train_set = windowed_dataset(temp, window_size=60, batch_size=100, shuffle_buffer=1000)
model = tf.keras.models.Sequential([
  tf.keras.layers.LSTM(60, return_sequences=True),
  tf.keras.layers.LSTM(60),
  tf.keras.layers.Dense(30, activation="relu"),
  tf.keras.layers.Dense(10, activation="relu"),
  tf.keras.layers.Dense(1),
])

optimizer = tf.keras.optimizers.SGD(lr=1.0000e-04, momentum=0.9)
model.compile(loss=tf.keras.losses.Huber(),
              optimizer=optimizer,
              metrics=["mae"])
history = model.fit(train_set,epochs=2)