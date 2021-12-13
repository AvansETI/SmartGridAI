# Applied research information
This document describes the results of the research that has been executed. The approach of the project, but also the sources and conclusions the project team has derived.

## Building controller objective
Within the Brains4Building project a lot of partners are working together to solve the same problem. The activities of this project will also be used as input for other work. While this project forms the input to the work of TUD, it is required to understand the objectives of TUD in this case. The TUD focus is on the multi-objective controller to optimize the building installations and meet the climate objectives. 

__The main objective of the controller is to track the energy balance in real-time based on the flexibility and constrainst of the building.__

For the controller it is important to characterise what is achievable within the building (flexibility). Based on data the building dynamics can be extracted and the limits of the building dynamics. In order to track the energy balance, the building installations are controller. Example of building installations can be a boiler, electrical storage and heat pumps. But also walls and windows have impact on the energy balance. Therefore, it is important to know how each component impacts the overal energy usage of the building. Or in our case, how each component impacts the indoor climate. A model is required that evaluates the situation quickly, so it can be used in a real-time manner. Large models could be used for training for example. 

Prediction of the indoor climate depends on many aspects, like occupancy, solar radiation and outside temperature. A model that is able to provide a prediction based on multiple variables is preferred. Another approach could be the detection of which installations are installed in the building with the use of data. Learning how these installations impact the indoor climate. A first aspect is to find out which aspects influences the indoor climate.

## Applied research question (IDEA)

### Cause
Building energy managent do not always lead to satisfied users. Furthermore, a lot of energy is lost by problems in the installation and configuration of these installations. A lot of improvement can be done to lower the energy usage and improve the comfort for the users.

### Problem statement
At this moment, energy management systems are not able to implement these improvement due to the fact that it is not clear how to approach this. Installations are typically not connected with each other. Data is not collected and building management systems only performs simple control tasks.

### Goal
The project takes four years and the goal is to big to solve within this project. This project aims for the prediction of the indoor climate based on the input of the building component (read installations) by applying machine learning concepts. The final proof-of-concept will be opensource software that is able to be configured with the required inputs, learn from historical data from these inputs and predict the target output. The target output could be temperature. If possible, more than one approach should be developed.

### Applied research question
Based on the information, the following central research question can be defined: __"How to develop machine learning based software, using real-time and historical data from building measurements and installations, to predict future evolvement of the indoor climate."__

The following sub-questions can be derived:
1. What so we understand under the term 'indoor climate'?
2. Which machine learning algoritms can be used for this type of predictions?
3. Which factors influences the indoor climate of a building?
4. What do we understand under "the prediction of target values"?
5. How should the software be designed, so it is able to learn from historical data and perform prediction of the target values?
6. Is it also possible to determine the future evolvement when the input is manually changed?

## Interesting links and people
* Markus Löning: PhD student focus on machine learning and time-series (https://www.youtube.com/watch?v=wqQKFu41FIw, https://github.com/alan-turing-institute/sktime)
* Time Series Analysis and Forecasting with Machine Learning: https://www.youtube.com/watch?v=AvG7czmeQfs
* SINDy: https://arxiv.org/abs/2004.02322

## ToDo

* Talk with Baldiri for sharing a dataset to perform the research in this field.
* Setup a meeting with Niel Yorke from TUD



Multivariate timeseries uses multiple timeseries input to make a forecast of a specific timeseries.
