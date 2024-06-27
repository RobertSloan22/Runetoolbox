import pandas as pd
import numpy as np
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import LabelEncoder, OneHotEncoder
from sklearn import model_selection
from sklearn.compose import ColumnTransformer
import matplotlib.pyplot as plt
import seaborn as sns
from sklearn.impute import SimpleImputer
import warnings
import os
from sklearn.metrics import accuracy_score
from sklearn.metrics import confusion_matrix
from sklearn.pipeline import Pipeline
from sklearn.model_selection import GridSearchCV
from sklearn.model_selection import RandomizedSearchCV
from scikeras.wrappers import KerasClassifier
import tensorflow as tf
from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import Dense
from tensorflow.keras.layers import Dense, Input, Dropout,BatchNormalization
from tensorflow import keras
from tensorflow.keras import layers
import random
from tensorflow.keras import backend

# Define training and validation data
train_data = features.loc[0 : train_split - 1]
val_data = features.loc[train_split:]

# Extract timestamps for plotting
train_timestamps = df[date_time_key].iloc[0:train_split].values
val_timestamps = df[date_time_key].iloc[train_split:].values

# Define the model
def create_lstm_model(input_shape, output_steps):
    inputs = keras.layers.Input(shape=input_shape)
    lstm_out = keras.layers.LSTM(32)(inputs)
    outputs = keras.layers.Dense(output_steps)(lstm_out)
    model = keras.Model(inputs=inputs, outputs=outputs)
    return model

# Get the input shape from the training data
sequence_length = int(past / step)
x_train = train_data.values
y_train = features.iloc[start:end][["price_usd"]]

dataset_train = keras.preprocessing.timeseries_dataset_from_array(
    x_train,
    y_train,
    sequence_length=sequence_length,
    sampling_rate=step,
    batch_size=batch_size,
)

x_val = val_data.iloc[:x_end].values
y_val = features.iloc[label_start:label_end][["price_usd"]].values

dataset_val = keras.preprocessing.timeseries_dataset_from_array(
    x_val,
    y_val,
    sequence_length=sequence_length,
    sampling_rate=step,
    batch_size=batch_size,
)

for batch in dataset_train.take(1):
    inputs_batch, targets_batch = batch
    input_shape = inputs_batch.shape[1:]
    output_steps = targets_batch.shape[1]

model = create_lstm_model(input_shape, output_steps)
model.compile(optimizer=keras.optimizers.Adam(learning_rate=learning_rate), loss="mse")

path_checkpoint = "model_checkpoint.weights.h5"
es_callback = keras.callbacks.EarlyStopping(monitor="val_loss", min_delta=0, patience=5)
modelckpt_callback = keras.callbacks.ModelCheckpoint(
    monitor="val_loss",
    filepath=path_checkpoint,
    verbose=1,
    save_weights_only=True,
    save_best_only=True,
)

history = model.fit(
    dataset_train,
    epochs=epochs,
    validation_data=dataset_val,
    callbacks=[es_callback, modelckpt_callback],
)

def visualize_loss(history, title):
    loss = history.history["loss"]
    val_loss = history.history["val_loss"]
    epochs = range(len(loss))
    plt.figure()
    plt.plot(epochs, loss, "b", label="Training loss")
    plt.plot(epochs, val_loss, "r", label="Validation loss")
    plt.title(title)
    plt.xlabel("Epochs")
    plt.ylabel("Loss")
    plt.legend()
    plt.show()

visualize_loss(history, "Training and Validation Loss")

# Prediction and Visualization
def show_plot(plot_data, delta, title):
    labels = ["History", "True Future", "Model Prediction"]
    marker = [".-", "rx", "go"]
    time_steps = list(range(-(plot_data[0].shape[0]), 0))
    future = list(range(1, delta + 1))

    plt.figure(figsize=(10, 6))
    plt.title(title)
    for i, val in enumerate(plot_data):
        if i == 0:
            plt.plot(time_steps, val, marker[i], label=labels[i])
        else:
            plt.plot(future, val, marker[i], markersize=10, label=labels[i])
    plt.legend()
    plt.xlim([time_steps[0], delta])
    plt.xlabel("Time-Step")
    plt.ylabel("Price (USD)")
    plt.show()

# Collect predictions and actual values for the entire validation set
predictions_list = []
true_values_list = []

for batch in dataset_val:
    x, y = batch
    predictions = model.predict(x)
    predictions_list.append(predictions)
    true_values_list.append(y)

# Convert lists to numpy arrays
predictions_array = np.concatenate(predictions_list, axis=0)
true_values_array = np.concatenate(true_values_list, axis=0)

# Denormalize predictions and true values
denorm_predictions = denormalize(predictions_array, data_mean[feature_keys.index('price_usd')], data_std[feature_keys.index('price_usd')])
denorm_true_values = denormalize(true_values_array, data_mean[feature_keys.index('price_usd')], data_std[feature_keys.index('price_usd')])

denorm_train_data = denormalize(train_data[["price_usd"]].values, data_mean[feature_keys.index('price_usd')], data_std[feature_keys.index('price_usd')])

# Plot training, validation data, and predictions using Plotly
def plot_training_and_predictions(train_data, true_values, predictions, train_timestamps, val_timestamps, title):
    fig = go.Figure()

    # Add traces for training data
    fig.add_trace(go.Scatter(
        x=train_timestamps,
        y=train_data.flatten(),
        mode='lines',
        name='Training Data'
    ))

    # Add traces for validation data (true)
    fig.add_trace(go.Scatter(
        x=val_timestamps[:len(true_values)],
        y=true_values.flatten(),
        mode='lines',
        name='Validation Data (True)'
    ))

    # Add traces for validation data (predicted)
    fig.add_trace(go.Scatter(
        x=val_timestamps[:len(predictions)],
        y=predictions.flatten(),
        mode='lines',
        name='Validation Data (Predicted)'
    ))

    # Update layout
    fig.update_layout(
        title=title,
        xaxis_title='Timestamp',
        yaxis_title='Price (USD)',
        legend_title='Legend'
    )

    fig.show()

plot_training_and_predictions(denorm_train_data, denorm_true_values, denorm_predictions, train_timestamps, val_timestamps, "Training Data and Model Predictions vs. True Values")
