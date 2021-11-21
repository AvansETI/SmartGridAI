# Project: Prediction of building climate for control optimization - part of project Brains4Buildings (2020 - 2021)
Within the current building automation systems the set points are fixed and controller for energy optimization is not used. Using the existing sensors it is difficult to control on a lower temperature and humidity to not sacrifice on comfort. A possible solution for this problem is to take prediction of certain measurements into account in order to deliver the right comfort on the right time. When it is not required, regulate on energy optimization. It is possible that more factors needs to take into account. For instance, when multiple people enter a room, the room will be heated up by these people. Therefore, the building automation system can anticipate on this and save energy. 

The goal of the project is to create opensource software, that is able to predict a timeseries measurement in the future, based on multiple inputs. This software can be used independently or by the controller. The software should be able to train, give good feedback on the quality of the training, and be used in (real-time) prediction mode.

The following applied research question has been defined: 
__“How could we predict future measurements concerning the internal climate of a building that can be used by the building automation controller and independently as prediction.”__

The following sub questions could be answered:
1.	What are the most important measurement that need to be predicted of the internal climate of a building?
2.	How should the prediction look like?
3.	Which datasets can be used to train, validate and test the algorithms?
4.	What kind of interface should be defined to integrate the software algorithm with the building automation controller?
5.	Which ML algorithms should be used to perform prediction of these timeseries measurements?
6.	How should the software be setup that it is user friendly and can be used by technical people with limited AI knowledge?
