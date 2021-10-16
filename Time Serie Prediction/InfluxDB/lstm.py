# -- IMPORTS --
import argparse
import configparser
from datetime import datetime
now = datetime.now()

config = configparser.ConfigParser()
config.read_file(open('config.ini'))
parser = argparse.ArgumentParser(description="Set options through the command line (takes priority over config file)")

# arguments
parser.add_argument("-a", "--activation", action="store", help="Set the activation function")
parser.add_argument("-b", "--batch-size", action="store", type=int, help="Set the batch size")
parser.add_argument("-c", "--checkpoint", action="store", type=int, help="Set the checkpoint (after nth epoch)")
parser.add_argument("-d", "--data", action="store", help="Set the location for the datasource")
parser.add_argument("-e", "--epoch", action="store", type=int, help="Set the number of epochs")
parser.add_argument("-lr", "--learning-rate", action="store", type=float, help="Set the learning rate")
parser.add_argument("-m", "--model", action="store", help="Set the location for an existing model")
parser.add_argument("-mn", "--model-name", action="store", help="Set the name for the model (default: data filename + timestamp)")
parser.add_argument("-p", "--predict", action="store_true", help="Predict with a given dataset (-d {path} or dataset in config required)")
parser.add_argument("-pn", "--prediction-name", action="store", help="Set the name for the prediction.csv (default: data filename + timestamp)")
parser.add_argument("-pml", "--plaidml", action="store_true", help="Enable PlaidML")
parser.add_argument("-r", "--resume", action="store", help="Resume training on existing model, filepath required")
parser.add_argument("-t", "--train", action="store_true", help="Train the model")
parser.add_argument("-v", "--verbose", action="store", type=int, help="Set the verbose")
args = parser.parse_args()

# PlaidML Imports - disable if you make use of cudnn
plaidml = args.plaidml or config.getboolean('Process', 'PlaidML')

# -- DATA --

data_location = args.data or config.get('Paths', 'DataLocation')

# determines whether we apply data analysis to the dataset.
do_analysis = config.getboolean('Process', 'PerformAnalysis')

# -- MODEL BUILDING --

# no. hours to forecast
n_forecasts = config.getint('Data', 'ForecastLength')

# determines how much data is used to forecast
n_input = n_forecasts * config.getint('Data', 'InputMultiplier')

# determines if the data will be scaled
use_scaled = config.getboolean('Data', 'ScaleData')

# determines whether we're going to train or evaluate an existing model
training = False if args.predict or args.resume else args.train if args.train else config.getboolean('Process', 'TrainModel')

# determines whether we're going to train a new model or continue training a existing model
resume_training = config.getboolean('Process', 'LoadExistingModel') if args.resume is None else True

# sets filepath where model gets saved / loaded from if resume_training = True
model_location = args.model or args.resume or config.get('Paths', 'ModelLocation')

# default naming format: {filename} + {current date (d-m-Y-H-M}. Example: filename-27-01-2021-12-30
filename = config.get('Paths', 'DataLocation').split("/")[-1].split(".")[0] + "-" + now.strftime("%d-%m-%Y-%H-%M")

# TODO: make use of names from config.ini (config.get('Names', 'ModelName') / config.get('Names', 'PredictionName'))
model_save_location = config.get('Paths', 'ModelSaveLocation') + (args.model_name or filename) + ".hdf5"

prediction_location = config.get('Paths', 'PredictionLocation') + (args.prediction_name or filename) + ".csv"

predict = args.predict or config.getboolean('Process', 'DoPrediction')

# -- HYPERPARAMETERS --

epochs = args.epoch or config.getint('HyperParameters', 'Epochs')

batch_size = args.batch_size or config.getint('HyperParameters', 'BatchSize')

verbose = args.verbose or config.getint('HyperParameters', 'Verbose')

learning_rate = args.learning_rate or config.getfloat('HyperParameters', 'LearningRate')

# determines after how many epochs the model gets saved (aka after each n-th epoch)
n_checkpoint = args.checkpoint or config.getint('HyperParameters', 'CheckpointInterval')

activation_function = args.activation or config.get('HyperParameters', 'ActivationFunction')

# FORECASTING
# seaborn chart sizes
figure_width, figure_height = 14, 5

# how many hours into the past should be displayed in the chart?
history_length = 72

import pandas as pd
import numpy as np
import os
# from influxdb import DataFrameClient

if plaidml:
    import plaidml.keras
    plaidml.keras.install_backend()
    os.environ["KERAS_BACKEND"] = "plaidml.keras.backend"
    os.environ['KMP_DUPLICATE_LIB_OK'] = 'True'
#     os.environ['PLAIDML_USE_STRIPE']='1'
#     os.environ['PLAIDML_VERBOSE']='1'

from sklearn.model_selection import train_test_split
from sklearn.preprocessing import MinMaxScaler

import matplotlib.pyplot as plt
import seaborn as sns
sns.set(rc={'figure.figsize':(figure_width, figure_height)})

from keras.models import Sequential, load_model
from keras.layers import Dense, LSTM, Dropout, TimeDistributed, RepeatVector
from keras.optimizers import Adam
from keras.callbacks import ModelCheckpoint

def to_supervised(train, n_input, n_output=8):
    X, y = list(), list()

    X_start = 0

    # iterate over train dataset
    for _ in range(len(train)):
        
        # set the ranges for input + output
        X_end = X_start + n_input
        y_end = X_end + n_output
        
        # check if data contains enough samples for sequence
        if y_end <= len(train):
            X.append(train[X_start:X_end, :])
            y.append(train[X_end:y_end, 0])
            
        X_start += 1
    assert len(X) > 0, "Unable to transform given data into a supervised format. \n train size: ({}), n_input+n_output: ({})".format(len(train), n_input+n_output)
    return np.array(X), np.array(y)

def build_model(data, n_input, params):
    
    # data preperation
    train, val = data
    X_train, y_train = to_supervised(train, n_input)
    X_val, y_val = to_supervised(val, n_input)
    
    # meta / parameters
    epochs, batch_size, verbose, learning_rate, n_checkpoint, model_location, resume_training, activation_function = params
    n_timesteps, n_features, n_outputs = X_train.shape[1], X_train.shape[2], y_train.shape[1]

    # reshape output
    y_train = y_train.reshape((y_train.shape[0], y_train.shape[1], 1))
    y_val = y_val.reshape((y_val.shape[0], y_val.shape[1], 1))
    
    
    if resume_training:
        model = load_model(model_location)
        print('loaded model from {}'.format(model_location))
    else:   
        model = Sequential()
        model.add(LSTM(256, activation=activation_function, input_shape=(n_timesteps, n_features)))
        model.add(Dropout(.4))
        model.add(RepeatVector(n_outputs))
        model.add(LSTM(256, activation=activation_function, return_sequences=True))
        model.add(Dropout(.2))
        model.add(LSTM(256, activation=activation_function, return_sequences=True))
        model.add(Dropout(.2))
        model.add(TimeDistributed(Dense(64, activation=activation_function)))
        model.add(TimeDistributed(Dense(64, activation=activation_function)))
        model.add(TimeDistributed(Dense(1, activation=activation_function)))
        opt = Adam(lr=learning_rate)
        model.compile(loss='mse', optimizer=opt)
        
    checkpoint = ModelCheckpoint(model_save_location, monitor='loss', verbose=1, save_best_only=True, mode='auto', period=n_checkpoint)
    history = model.fit(X_train, y_train, epochs=epochs, batch_size=batch_size, verbose=verbose, validation_data=(X_val, y_val), callbacks=[checkpoint], shuffle=False)
    
#     model.save(os.path.join(wandb.run.dir, "model.h5"))
    
    # plot the model
    # plt.plot(history.history['loss'])
    # plt.plot(history.history['val_loss'])
    # plt.plot(history.history['accuracy'])
    # plt.title('model loss')
    # plt.ylabel('loss')
    # plt.xlabel('epoch')
    # plt.legend(['train', 'validation'], loc='upper right')
    # plt.show()
    
    return model

def forecast(model, history, n_input):
    data = np.array(history)
    X = data[-n_input:, :]
    X = X.reshape((1, X.shape[0], X.shape[1]))
    yhat = model.predict(X, verbose=0)
    yhat = yhat[0]
    return yhat

def visualize_forecast(history, validation, future, pred, future_pred, n_input, n_forecasts, history_length=48):
    if n_input > history_length:
        past = history[-history_length:-n_forecasts+1]
    else:   
        past = history[-n_input:-n_forecasts+1]
    
    future = future[-n_forecasts:]
    validation = validation[-n_forecasts:]

    validation.index = validation.index + pd.Timedelta(n_forecasts, unit='h')
    future.index = future.index + pd.Timedelta(n_forecasts, unit='h')

    future['Prediction'] = future_pred
    validation['Prediction'] = pred
    validation['Actual'] = history[-8:]['Actueel verbruik']
    
    sns.lineplot(data=past, x=past.index, y="Actueel verbruik")
    sns.lineplot(data=validation, x=validation.index, y="Actual", color="lime")
    sns.lineplot(data=validation, x=validation.index, y="Prediction", color="red")
    sns.lineplot(data=future, x=future.index, y="Prediction", color="darkred")
    plt.legend(['Actueel verbruik (Past)','Actueel verbruik (Actual)','Actueel verbruik (Prediction)', 'Actueel verbruik (Future Prediction)'])

    plt.title('Predictions of Actueel verbruik')
    plt.xlabel('Timeline')
    plt.ylabel('Actueel verbruik')
    plt.grid(which='major', color="#ffffff", alpha=.5)
    plt.axvline(x=past.index[-1], color="green", linestyle="--")
    plt.axvline(x=validation.index[-1], color="green", linestyle="--")
    plt.show()
    
def to_datetime(timestamp):
    return np.datetime64(timestamp)

def output_data(data, predictions, n_forecasts):
    data = data[-n_forecasts:]
    data['Prediction'] = predictions
    data = data['Prediction']
    return data

#####################################
# Maurice: TRY InfluxDB integration #
#####################################
# the keys are different, consumption_kw, consumption_t1_kwh and consumption_t2_kwh
#
# client = DataFrameClient(host='localhost', port=8086)
# client.switch_database('smartgridai')
# q = "select * from datasets"
# result = client.query(q)
# print(result["datasets"])

data = pd.read_csv(data_location, index_col='Timestamp')
# data = result["datasets"]
data.index = data.index.map(to_datetime)
# data['Totaal vermogen ontvangen'] = data['consumption_t1_kwh'] + data['consumption_t2_kwh']
data['Totaal vermogen ontvangen'] = data['Totaal vermogen ontvangen in tariff 1 in KWH'] + data['Totaal vermogen ontvangen in tariff 2 in KWH']

if do_analysis:
    columns = [x for x in data.columns if x in ['Actueel verbruik in KW', 'Totaal vermogen ontvangen in tariff 1 in KWH', 'Totaal vermogen ontvangen in tariff 2 in KWH', 'Totaal vermogen ontvangen']]
    data_resample = pd.DataFrame(columns=columns)
    data_resample['consumption_kw'] = data['consumption_kw'].resample('h').mean()
    data_resample['consumption_t1_kwh'] = data['consumption_t1_kwh'].resample('h').max()
    data_resample['consumption_t2_kwh'] = data['consumption_t2_kwh'].resample('h').max()
    data_resample['Totaal vermogen ontvangen'] = data['Totaal vermogen ontvangen'].resample('h').max()

    print("Number of rows: {} \n".format(len(data_resample)))
    print("Number of rows (NaN excluded): {} \n".format(len(data_resample[~np.isnan(data_resample['Totaal vermogen ontvangen'])])))
    print("")
    print("Days in dataset (after setting index):")
    for x in data_resample.resample('d').mean().index:
        print("  ", x)
    print("\nDays with NaN's:")
    for x in data_resample[np.isnan(data_resample['Totaal vermogen ontvangen'])].resample('d').mean().index:
        print("  ", x)
    print("\n")
    # sns.boxplot(x=data_resample.index.hour, y=data_resample['consumption_kw'])
    # plt.xlabel('Time in hours')
    # plt.show()
    # sns.boxplot(x=data_resample.index.day, y=data_resample['consumption_kw'])
    # plt.xlabel('Time in days')
    # plt.show()

df = pd.DataFrame()
# set to mean to get kw/h, sum for kw.
df['Actueel verbruik'] = data['Actueel verbruik in KW'].resample('h').mean()
# df['Actueel verbruik'] = data['consumption_kw'].resample('h').mean()

# remove NaN's from dataset
df = df[~np.isnan(df['Actueel verbruik'])]

# add time-related information to dataset
df['Month'] = df.index.month
df['Week'] = df.index.week
df['Day'] = df.index.day
df['Hour'] = df.index.hour
# df['Totaal vermogen ontvangen'] = data['Totaal vermogen ontvangen'].resample('h').max()

df.head()

# Fill NaN's with column's mean value
for j in range(0, len(df.columns)):
    df.iloc[:, j] = df.iloc[:, j].fillna(df.iloc[:, j].mean())

df_future = df[-n_input:]
df_pred = df[-(n_input+n_forecasts):-n_forecasts]
df_resample = df[:-n_forecasts*2]

if use_scaled:
    scaler = MinMaxScaler()
    df_pred_scaled = scaler.fit_transform(df_pred)
    df_future_scaled = scaler.fit_transform(df_future)
    train, val = train_test_split(scaler.fit_transform(df_resample), test_size=.4, shuffle=False, stratify=None)
else:
    train, val = train_test_split(df_resample.values, test_size=.4, shuffle=False, stratify=None)

if training or resume_training:
    # throw error if n_input is too big
    assert n_input+n_forecasts < len(val), "n_input + n_forecasts ({}) is larger than the amount of validation samples ({}) ".format(n_input+n_forecasts, len(val))

    data = [train, val]
    params = [epochs, batch_size, verbose, learning_rate, n_checkpoint, model_location, resume_training, activation_function]
    model = build_model(data, n_input, params)
else:
    model = load_model(model_location)


# write prediction
if predict:
    if use_scaled:
        pred = forecast(model, df_pred_scaled, n_input)
        future = forecast(model, df_future_scaled, n_input)

        _ = np.zeros([len(pred), len(df_pred.columns)])

        _[:, 0] = np.squeeze(pred)
        pred = scaler.inverse_transform(_)

        _[:, 0] = np.squeeze(future)
        future_pred = scaler.inverse_transform(_)

#       visualize_forecast(df, df_pred, df_future, pred[:, 0], future_pred[:, 0], n_input, n_forecasts, history_length)

    else:
        pred = forecast(model, df_pred, n_input)
        future_pred = forecast(model, df_future, n_input)

        # Prepare dataframes for plotting
        # visualize_forecast(df, df_pred, df_future, pred, future_pred, n_input, n_forecasts, history_length)

    output_data(df_future, future_pred, n_forecasts).to_csv(prediction_location, index=True)
    print("saved predictions at {}".format(prediction_location))
