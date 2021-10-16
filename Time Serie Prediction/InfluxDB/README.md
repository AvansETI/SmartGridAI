# lstm.py

## Getting started
### Prerequisites
- An (preferably empty) environment with python 3.7.9 or higher.
### Installing packages
#### CPU Training
run: `pip install -r requirements-cpu.txt`
#### GPU Training
##### Nvidia
run: `pip install -r requirements-gpu-nvidia.txt`

Afterwards, follow the steps in the section [Setting up an NVIDIA environment](https://github.com/macsnoeren/SmartGridAI/tree/console/Time%20Serie%20Prediction/InfluxDB#setting-up-an-nvidia-environment).
##### AMD (PlaidML)
*"PlaidML is an advanced and portable tensor compiler for enabling deep learning on laptops, embedded devices, or other devices where the available computing hardware is not well supported or the available software stack contains unpalatable license restrictions."*

see the [PlaidML git repository](https://github.com/plaidml/plaidml#quick-start) on how to get started with PlaidML.

*note: you're also able to use PlaidML to accelerate your CPU*

run: `pip install -r requirements-gpu-amd.txt`

Use the `-pml` or `-plaidml` argument when training

## Running the script
In order to run the script, use `python lstm.py`, this will start the script and it will make use of the configuration file.

Arguments can be added to the command, resulting in the script running and setting values from the arguments while filling the missing values with the settings given in `config.ini`.
An example of using extra arguments in the command line would be: `python lstm.py --train --data data.csv --epochs 1000 --batch-size 32`.

For information on how to configure settings, see the section "Configuration" below.


## Configuration

### Configuration file
Within this repository you'll find a file named `config.ini` which consists of the following content:
```ini
[Paths]
ModelLocation = model.hdf5
ModelSaveLocation = ./models/
DataLocation = ../data/data.csv
PredictionLocation = ./predictions/

[Names]
ModelName = firstmodel
PredictionName = firstprediction

[Process]
PlaidML = no
PerformAnalysis = no
TrainModel = no
LoadExistingModel = no
DoPrediction = no

[Data]
ScaleData = no
ForecastLength = 8
# InputMultiplier sets n_input, which is ForecastLength * InputMultiplier
InputMultiplier = 4

[HyperParameters]
Epochs = 100
BatchSize = 8
Verbose = 1
LearningRate = 0.0001
ActivationFunction = relu
# Sets which nth epoch we save the model (if it has improved compared the previous one)
CheckpointInterval = 100
```

### Arguments
An alternative to the configuration file is to make use of these arguments that you can pass on through the CLI: 

| Argument | Information |
|---|---|
| `-h`, `--help`  | Shows the help message in console  |
| `-a VALUE`, `--activation VALUE`| Set the activation function used within the model  |
| `-b VALUE`, `--batch-size VALUE` | Set the batch size  |
| `-c VALUE`, `--checkpoint VALUE`  | Set the checkpoint at which the model saves the current weights  |
| `-d VALUE`, `--data VALUE`  | Set the location for the data source  |
| `-e VALUE`, `--epochs VALUE`  | Set the number of epochs  |
| `-lr VALUE`, `--learning-rate VALUE`| Set the learning rate |
| `-m VALUE`, `--model VALUE`| Set the location for an existing model|
| `-mn VALUE`, `--model-name VALUE`| Set the name for the to-be-saved model|
| `-p`, `--predict`| Make a prediction. Requires set filepath for dataset |
| `-pn VALUE`, `--prediction-name VALUE`| Set the name for the to-be-saved prediction (.csv file) |
| `-pml`, `--plaidml`| Enable PlaidML backend. see the [PlaidML git repository](https://github.com/plaidml/plaidml) for more information.|
| `-r VALUE`, `--resume VALUE`| Resume training with existing model. Requires model filepath.|
| `-t`, `--train`| Enable training |
| `-v VALUE`, `--verbose VALUE`| Set the verbose (either 0, 1 or 2)|

Making use of arguments will **not** override any configurations set within `config.ini`, but they will take priority over any existing settings within the configuration file. 
Making use of only the command line will provide you with limited functionality (as not everything from the config file has been made available through arguments as of now), meaning that the script will still use the config file to retrieve the missing values.

## Data
The model makes use of sequences of data as input, meaning that multiple rows of data are required to get a single prediction.

A few examples as to how the data would be set up:

| X | y |
|---|---|
| [1,2,3,4,5,6,7,8] | [9,10,11,12,13,14,15,16] |
| [2,3,4,5,6,7,8,9] | [10,11,12,13,14,15,16,17] |
| [3,4,5,6,7,8,9,10] | [11,12,13,14,15,16,17,18] |
| [4,5,6,7,8,9,10,11] | [12,13,14,15,16,17,18,19] |
| [5,6,7,8,9,10,11,12] | [13,14,15,16,17,18,19,20] |

The amount of data required to fill X and y with is customizable through the configuration file; `ForecastLength` sets the amount of forecasts in steps for y (default = 8) and also serves as the minimum amount of data required for X. `InputMultiplier` sets the multiplier used for X. We recommend using at least 3 times the amount of data used in y, as this improve the models ability to find trends within the dataset. **When making a prediction these 2 variables need to be on the set on the values used when the given model was trained, else the application will not work**.

Increasing `InputMultiplier` will require more memory and might result in exceptions.
## Limitations

### Error handling
We have added a limited amount of assertions that validate whether there is enough data in the given dataset, but besides this there is a lack of error handling from our side.

### InfluxDB
lstm.py - as of right now - doesn't provide any functionality that connects to an influxdb database and read/writes data. There are two scripts included in the repository `influx_import.py` and `influx_read.py` which provides a good basis if one desires to implement these features. 

### Model saving
As of right now, the configuration file has an unused Names section, meaning that the values set won't be used within the python script.
If no name is provided through the command line, the script will make use of the following naming scheme: `{data source name}-{%d-%m-%Y-%H-%M}`.

*Please note that the same applies for the predictions (the exported .csv file).*

### WanDB
Integration of WanDB within our script has been removed, if you would like to add WanDB logging back, please refer to the .ipynb notebooks within the LSTM folder.

### Dropout layers
Due to the limited dataset we're working with, we've decided to add dropout layers to help with preventing overfitting. In the future one should consider removing these layers when more data has been made available.

An explanation about dropout layers can be found [here](https://machinelearningmastery.com/dropout-for-regularizing-deep-neural-networks/).
## Setting up an NVIDIA environment
1. Install latest Nvidia Drivers from Geforce Experience: https://www.nvidia.com/nl-nl/geforce/geforce-experience/

2. Download CUDA 11.0 from here: https://developer.nvidia.com/cuda-11.0-download-archive

3. When installing CUDA 11.0 choose custom installation and make sure ONLY CUDA is checked

4. In "C:/Program Files/Nvidia GPU Computing Toolkit/CUDA" replace all files with the files within the `./cuda_replacement_11.0/` folder.

5. In your conda environment run: "conda install tensorflow-gpu==2.1.0" *(not necessary if you run requirements-gpu-nvidia.txt)*

## Troubleshooting
#### Nvidia troubleshoot tip:
```
tensorflow.python.framework.errors_impl.InternalError:  Blas GEMM launch failed : a.shape=(8, 256), b.shape=(256, 1024), m=8, n=1024, k=256
         [[{{node lstm_1/while/body/_1/MatMul_1}}]] [Op:__inference_keras_scratch_graph_4427]
```

The error above means your GPU is most likely in use by another program.

#### All predictions made by the model are 0
As far as we know with the issue, this is usually caused by an extremely underfit model. things you can try:
- add more layers to create a more complex model within `lstm.py`
- increase the amount of epochs used during training (our findings suggest that a proper LSTM model should require at least 1000 epochs.)
- lower the batch size, we've had the best results with a batch size of 8, large batch sizes might require compensation by increaing the amount of epochs and learning rate.
