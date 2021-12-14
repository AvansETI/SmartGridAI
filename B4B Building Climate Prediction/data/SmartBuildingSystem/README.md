# Smart Building System Dataset

[Dataset from Kaggle](https://www.kaggle.com/ranakrc/smart-building-system)

## Description
The dataset used in our AISTATS'17 work contains the data for 5 different types of measurements from 50 rooms in an office building.

Each room includes 5 types of measurements: CO2 concentration, room air humidity, room temperature, luminosity, and PIR motion sensor data.

Each file contains the time stamps (in Unix Epoch Time) and actual readings from the sensor.

If you use the dataset, please consider citing the following paper:
		Dezhi Hong, Quanquan Gu, Kamin Whitehouse.
		High-dimensional Time Series Clustering via Cross-Predictability.
		In AISTATS'17

## Purpose
This dataset is used for time series prediction of optimizing building climate. You can find the repo here if you are interested. The original data has been transformed to be used for the transformer network in pytorch forecasting and pytorch lightning.