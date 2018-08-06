import tensorflow as tf
from tensorflow import keras
import numpy as np

import mlflow
from mlflow import tracking

# load dataset
dataset = np.loadtxt("/Users/wzhuang/housing.csv", delimiter=",")

# save the data as artifact
mlflow.log_artifact("/Users/wzhuang/housing.csv")

# split the features and label
X = dataset[:, 0:15]
Y = dataset[:, 15]

# define the model
model = keras.Sequential([
    keras.layers.Dense(64, activation=tf.nn.relu, 
                       input_shape=(X.shape[1],)),
    keras.layers.Dense(64, activation=tf.nn.relu),
    keras.layers.Dense(1)
  ])
  
# log some parameters
mlflow.log_param("First_layer_dense", 64)
mlflow.log_param("Second_layer_dense", 64)

optimizer = tf.train.RMSPropOptimizer(0.001)

model.compile(loss='mse',
              optimizer=optimizer,
              metrics=['mae'])

# train
model.fit(X, Y, epochs=500, validation_split=0.2, verbose=0)

# log the model artifact
model_json = model.to_json()
with open("model.json", "w") as json_file:
    json_file.write(model_json)
mlflow.log_artifact("model.json")
