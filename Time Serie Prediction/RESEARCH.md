# Research into time series predictions

## Algorithms

In our project we plan to use a machine learning algorithm for time series predictions. We will take a closer look at a variety of machine learning algorithms. However we must prove our new found machine learning algorithms against a more traditional approach. To do this we will also research what classic algorithms were/are used to do time series predictions without the use of machine learning.

We've decided to look into the following algorithms:
*   SARIMAX
*   CNN
*   GRU
*   LSTM

### Seasonal Autoregressive Integrated Moving Average (SARIMAX)
SARIMAX, or Seasonal ARIMA with exogenous variables is an extension of the Autoregressive Integrated Moving Average (ARIMA) model and it is able to give forecasts based on seasonal data. The standard ARIMA model is capable of forecasting univariate time series data without seasonal components (Brownlee, 2020a, 2020b). 

Due to the lack of support for seasonal data, which we deem to be an important feature, as the data will be affected by seasonal changes, such as the earth’s tilt on its axis, which impacts the duration of daylight (National Weather Service, n.d.), we believe that ARIMA would not be able to provide us with (highly) accurate forecasts, where SARIMAX will have a better chance of being able to provide us with more accurate forecasts by implementing three hyperparameters to specify models for the seasonal component of the series and by adding an additional parameter for the period of the seasonality (Brownlee, 2019). 

A downside to SARIMAX is that it can only handle univariate time series, which may, depending on the input data, make this algorithm unsuitable for our needs. An alternative algorithm that would be able to forecast multivariate time series is VAR or VARMA, but those lack the ability to predict time series with trend or seasonal components (Brownlee, 2020b).

The SARIMAX model will serve as our ‘classical’ model which we will use to benchmark the trained models of the neural networks.

### Convolutional Neural Network (CNN)
Normally a CNN would be used for image-related predictions, but it can be used for other applications, such as time series prediction, as shown by Brownlee (2020c), CNNs can be used for univariate, multivariate and multi-step time series predictions. 

A potential downside of implementing a CNN is that it would require us to alter the dataset, which might devalue the network when measuring results to required effort in contrast with other neural network implementations. 

### Gated Recurrent Unit (GRU)

GPU optimization is important for us to train our model. Tensorflow 2.0 supports CuDNNGRU out of the box. This is a specialized LSTM layer we can utilize to optimize training with a GPU. In Tensorflow 1.0 you had to specifically state that you wanted to use a CuDNNGRU layer, in 2.0 any LSTM layer is automatically a CuDNNGRU Layer. However this does have limitations making any of the following changes will make Tensorflow use a standard LSTM layer and run it on the CPU.

*   Changing the activation function from tanh to something else.
*   Changing the recurrent_activation function from sigmoid to something else.
Using recurrent_dropout > 0.
*   Setting unroll to True, which forces LSTM/GRU to decompose the inner tf.
*   while_loop into an unrolled for loop.
*   Setting use_bias to False.
*   Using masking when the input data is not strictly right padded (if the mask corresponds to strictly right padded data, CuDNN can still be used. This is the most common case).

### Long Short-Term Memory (LSTM)

As with GRU, GPU optimization is important for us to train our model. Tensorflow 2.0 supports CuDNNLSTM out of the box. This is a specialized LSTM layer we can utilize to optimize training with a GPU. In Tensorflow 1.0 you had to specifically state that you wanted to use a CuDNNLSTM layer, in 2.0 any LSTM layer is automatically a CuDNNLSTM Layer. The same limitations as with GRU apply here.


## Dashboard

In order to show our predictions and data to the user, we would like to use a dashboard. We can make a dashboard from scratch. However, we saw that there are a lot of companies who can provide us with good software to create these dashboards. One of the many softwares we've seen was Grafana. In order to see what Grafana has to offer, we've decided to take a look at their website and their documentation to see if this software can provide us with the right tools and functionalities.

###Grafana Research
This is our research on what Grafana has to offer. These notes will give us a quick overview on what we saw as interesting features that we can implement for our project.
As seen in Grafana Features and Shivang ( 2020).

####What is Grafana?
Grafana is an open source platform where you can show data in a dashboard. This way a user can see all the necessary data without having to navigate through different views or dashboards. We used Grafana’s documentation and their playground to explore all the functionalities they offer. 

####Grafana functionality
- Real-time edits will be shown immediately in the dashboards
- Notifications. This will come in handy to make a log about all the big changes happening to the algorithm's score, temperatures, etc.
- Multiple resources per graph. This way, we can compare and show the predicted values with the real-time values to see how accurate our predictions are.
- Build-in Influx DB support. We would like to use a time-series database. According to the research, Influx DB is a good database to use for this project. Grafana has support for Influx DB which would help us save time on trying to connect a database to our dashboard.
- Functionality annotations. This is something we can use for our graphs. We would like to show certain values per certain timespan. According to their demo dashboard, we can use different annotations from 1 minute to maximum 24 hours. This way, the user can easily see what the certain timespan is.
- Designing in Grafana is very simple; you can place a board on the screen and stretch and move it to your liking. You can place an object in that board to show certain values. This way, it's simple to create a design for our dashboard without using any coding to position it.
- Use of bar gauges. Grafana has the option to use a bar gauge to show certain data values. We can use this to show our average prediction accuracy, wattage, temperatures, etc. However, for some data this could not be simply used since bar gauges are based on a maximum and a minimum values.
- Grafana’s way of showing the user what the data presents is a great way to let any type of user know what these values are meant to be.
- Grafana also gives the creators the opportunity to use different kinds of graphs to make sure we can use the best type of graph to show our data to the user. One that was interesting to use is the “Null point mode”. This way we can compare our prediction with the actual usage and the accuracy in one graph. This way, it’s easier for the user to comprehend why these predictions are good or bad. The “Null point mode” works the same as a box plot we use earlier on in the minor for the Titanic survival rate casus.
- Grafana uses lazy loading to show data in a suited format for the given data. This way we don’t have to worry about sizing and scaling.
- Gafana has an option to combine different kinds of resources in one panel/board. They give an example combining InfluxDB,Elastic and Graphite.
- Multiple resources; we can use multiple boards with different time spans on the same data. This way we can, for example, show our predictions for 10 minutes, 6 hours and 24 hours.
- We noticed that the tool can also provide us an inside on how the databases are responding to our actions on the board. Maybe we can use this to see the activity of our resources.
- The tool has an option to filter the board however, this is hidden away in a corner away from the dashboard. Maybe we can see if there is an option to create filters within the dashboard for the user to click on.
- Grafana’s dashboard has the option to create preset dashboards. This way we can show different kinds of board so that the user can decide what type of dashboard they would like to see.
- The tool also has an option to implement their cloud service. This is a fast fully managed open SaaS, Software as a Service, platform.

After being able to write data to our database and using that data in Grafana, we've found out that for some reason we are not able to create a custom time range for each panel; the dashboard itself uses a time range. This timerange will be used in all of the created panels. This means that when we would like to show our 24 hours worth of data, it will be shown in the range given to the dashboard. For now, we've decided to leave it as it is due to InfluxDB being the main focus of these two programs.

The problem might be due to the newest version of Grafan we are using; when we were troubleshooting our problem, a lot of people have foundn a solution for it. The weird part being that the solution is in Grafana itself. However, we are using Grafana V2.0 and all of the solutions are found in an older version (V1.8/V1.7).

We also found out that, for some weird reason, we could only get the connection to work if we work via Flux instead of using the common type InfluxQL; we would not be able to get a connection with our InfluxDB bucket via InfluxQL due to some bad request. Using InfluxQL to query our data in our created panels would have been easier to work it. It would also help with troubleshooting bad queries due to the amount of solutions and problems created in InfluxQL. InfluxQL compared to Flux uses the same format as SQL, a language we all know due to our experience working with this language for some project in our chosen education. Flux however, has it's own coding language and format which we all have never worked with before.


### Database

In order to feed data to the dashboard, we will be making use of an InfluxDB database. InfluxDB is a time series database that is optimized for time-stamped or time series data (InfluxData, n.d.-b) which is beneficial for us, because the majority of the data that we will be working with is time series data. InfluxDB also increases query and write performance, by restricting update and delete permissions (InfluxData, n.d.-a). Updating rows of data is rarely done within a time series database and deleting data is mostly done on old and obsolete data, which can help us with achieving lower waiting times between predicting and projecting the data.

Another benefit from working with InfluxDB is that the dashboard that we plan to use, Grafana, ships with a feature-rich data source plugin for InfluxDB (Grafana Labs, n.d.-b), thus making InfluxDB a great fit to our needs.

InfluxDB is not for beginners; we all have never used InfluxDB and when we're following the guides and tutorials to set everything up, there was little to nothing to find on how to write data to InfluxDB. We had a lot of problem trying to write our data to InfluxDB and when we were troubleshooting them, we couldn't find a lot of solutions or help for our common problems. We eventually found or solutions, but it has taken us quite a while to find it. Thus, concluding that InfluxDB works well once you know how it works. There may be a different platform to use for our purpose with a better platform to explain the steps for even the newest programmers.

One of our problems was our timestamp; we thought that InfluxDB uses that normal and common format of timestamps. After some long research and troubleshooting we've found out that they want us to send the timestamp in nanoseconds. This was something we did not have encountered before and this was never explained in the given guides from InfluxDB. We've made a converter for our data in order to work with converting the timestamp and posting it in our database.

We have tried different ways to import data to InfluxDB; We've tried using CSV files, text files, etc. We eventually found out a automated way to write data to our database (Bucket as they call it).


# References

Brownlee, J. (2019, August 21). A Gentle Introduction to SARIMA for Time Series Forecasting in Python. Retrieved November 19, 2020, from https://machinelearningmastery.com/sarima-for-time-series-forecasting-in-python/

Brownlee, J. (2020a, August 19). How to Create an ARIMA Model for Time Series Forecasting in Python. Retrieved November 19, 2020, from https://machinelearningmastery.com/arima-for-time-series-forecasting-with-python/

Brownlee, J. (2020b, August 20). 11 Classical Time Series Forecasting Methods in Python (Cheat Sheet). Retrieved November 19, 2020, from https://machinelearningmastery.com/time-series-forecasting-methods-in-python-cheat-sheet/

Brownlee, J. (2020c, August 28). How to Develop Convolutional Neural Network Models for Time Series Forecasting. Retrieved November 19, 2020, from https://machinelearningmastery.com/how-to-develop-convolutional-neural-network-models-for-time-series-forecasting/ 

Grafana Labs. (n.d.-a). Grafana Play. Retrieved November 19, 2020, from 
https://play.grafana.org/d/000000012/grafana-play-home?orgId=1 

Grafana Labs. (n.d.-b). InfluxDB. Retrieved November 19, 2020, from https://grafana.com/docs/grafana/latest/datasources/influxdb/

InfluxData. (n.d.-a). InfluxDB design principles | InfluxDB OSS 2.0 Documentation. Retrieved November 19, 2020, from https://docs.influxdata.com/influxdb/v2.0/reference/key-concepts/design-principles/

InfluxData. (n.d.-b). Time Series Database (TSDB) Explained | InfluxDB. Retrieved November 19, 2020, from https://www.influxdata.com/time-series-database/

Grafana Features. (n.d.) Grafana Labs. Retrieved November 19, 2020, from
https://www.grafana.com/grafana

Shivang (2020, August 13). What is Grafana? Why Use It? Everything You Should Know About It. 8bitmen.Com. https://www.8bitmen.com/what-is-grafana-why-use-it-everything-you-should-know-about-it/

Recurrent Neural Network with Keras. Retrieved November 20, 2020, from https://www.tensorflow.org/guide/keras/rnn

National Weather Service. (n.d.). What Causes the Seasons? Retrieved November 19, 2020, from https://www.weather.gov/fsd/season 

Annotated CSV | InfluxDB Cloud Documentation. (n.d.). InfluxData. Retrieved 7 January 2021, from https://docs.influxdata.com/influxdb/cloud/reference/syntax/annotated-csv/

Dotis, A. (2018, July 2). Getting Started: Writing Data to InfluxDB. Medium. https://medium.com/@dganais/getting-started-writing-data-to-influxdb-54ce99fdeb3e

InfluxDB Line Protocol Bad Timestamp. (2019, February 13). Stack Overflow. https://stackoverflow.com/questions/44106683/influxdb-line-protocol-bad-timestamp/54559973#54559973

Learn about InfluxDB OSS. (n.d.). InfluxData. Retrieved 4 January 2021, from https://docs.influxdata.com/influxdb/v1.8/introduction/

With Grafana. (n.d.). Grafana Labs. Retrieved 4 January 2021, from https://grafana.com/docs/grafana/latest/getting-started/getting-started/

Write data to InfluxDB | InfluxDB OSS 2.0 Documentation. (n.d.). InfluxData. Retrieved 8 January 2021, from https://docs.influxdata.com/influxdb/v2.0/write-data/#timestamp-precision

```python

```
