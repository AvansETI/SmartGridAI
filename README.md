# SmartGridAI
SmartGrid AI is a research area that applies artificial intelligence within the context of the energy transition. It is a research topic from the research groups Smart Energy and Datascience & ICT. Started with our own funding to get up to speed, we have dived into reinforcement learning and prediction of time series. At this moment, we are involved in a larger project that is focussing on building automation and energy optimization based on big data approached. Two projects have been started to support this project.

# Project: Prediction of building climate for control optimization - part of project Brains4Buildings (2020 - 2021)
Within the current building automation systems the set points are fixed and controller for energy optimization is not used. Using the existing sensors it is difficult to control on a lower temperature and humidity to not sacrifice on comfort. A possible solution for this problem is to take prediction of certain measurements into account in order to deliver the right comfort on the right time. When it is not required, regulate on energy optimization. It is possible that more factors needs to take into account. For instance, when multiple people enter a room, the room will be heated up by these people. Therefore, the building automation system can anticipate on this and save energy. 

The goal of the project is to create opensource software, that is able to predict a timeseries measurement in the future, based on multiple inputs. This software can be used independently or by the controller. The software should be able to train, give good feedback on the quality of the training, and be used in (real-time) prediction mode.

The following applied research question has been defined: __“How could we predict future measurements concerning the internal climate of a building that can be used by the building automation controller and independently as prediction.”__

The following sub questions could be answered:
1.	What are the most important measurement that need to be predicted of the internal climate of a building?
2.	How should the prediction look like?
3.	Which datasets can be used to train, validate and test the algorithms?
4.	What kind of interface should be defined to integrate the software algorithm with the building automation controller?
5.	Which ML algorithms should be used to perform prediction of these timeseries measurements?
6.	How should the software be setup that it is user friendly and can be used by technical people with limited AI knowledge?

# Project: Prediction of human wellbeing for building optimization - part of project Brains4Building (2020 - 2021)
Within the B4B project we would like to execute an applied research project in the field of how AI can be applied to get more information about the user satisfaction, comfort and interaction within building. This information should lead to building improvements of the building automation, but also a way to inform the users how to use the building to get more comfort. An example is that the building automation could create a specific comfort condition in one part of the building and a different one in another part of the building. 

During a  separate consortium meeting at 16 September 2021 we have zoomed into the possible applied research questions we would like to do within this student project. This document is the outcome of this meeting and will be the starting point for the students to start with the project. All participant are willing to create an ”expert” project board that can be used by the students to get data sets, steering and information that is important for a successful project. Eventually the students will articulate themselves the final applied research question(s) and goal(s) to execute the project and create the necessary results for the project.

Four ideas have been discussed during the meeting:
1.	Human interface to measure subjective comfort and experience of how people feel, how to people respond to and how to get information from people. The goal is to get a grip on how people feel and how this can be used to further optimize the building automation system. It would be nice to create a permanent feedback loop. Feedback of the people can be active or passive. Examples of active feedback could be done by using app’s and push buttons. Passive feedback is for example using camera’s to see if people are happy or by means of temperature and humidity. This is a continuous game finding the balance between users/buildings.
2.	Mapping objective and passive measurements. Using machine learning to see if there is a correlation between objective measurements and how people feel. Different objective sources can be used.
3.	To determine the objective criteria, besides temperature and relative humidity, that correlates with the wellbeing or satisfaction of people. For example noise, smell, light and CO2 could be used.
4.	A lot of data is available within buildings and can be used to measure the movement of people of instance. An example is the elevator movement that can be used. It would be nice to see what data is really needed. The goal is not having an optimal set, but more to see what could be used that is already available within buildings.

There are existing models the model how people feel. Unfortunately, these models have a mismatch what people actually feel. How could we measure the comfort of people. Furthermore, getting feedback from people is difficult. Usually the people that are not satisfied  use these feedback tools. Transforming these feedback tools into complaint tools. Therefore, the feedback is not matched with the real situation.  How to get correct and good feedback from people is therefore a good research topic. Furthermore, people are willing to cooperate to give feedback for example two weeks. However, when the feedback period takes much longer, the people get less willingness.

Another aspect that is seen is that people are happy while the building comfort is not good. In this case, other elements like working at a good company, count largely for the wellbeing of the people. Finding the balance for the whole or individual is a challenging task. It is needed to find a balance that suits everybody. At the other hand, it is also possible to meet individual people in different areas of the building.

It can be concluded that comfort is not only measuring temperature and humidity. Al lot can play a role in the wellbeing of the people. Influencing people to get more comfort is also possible. So, it could also be about the interaction between the building and the people.

At the end of the meeting we have tried to get a first idea of the project assignment in terms of an applied research question. The students are able to define the final applied research question(s) for their project. However, we would like to provide a good starting point. The following has been discussed:
1.	What kind of data should we collect to be able to measure the comfort and wellbeing of the people?
2.	How could we collect this data actively and passively to measure the comfort and wellbeing of the people?
3.	What are the objective criteria we should match against?
4.	Can we use machine learning to find patterns between the objective measurements and subjective comfort/wellbeing of the people?

The goal is to find which machine learning algorithm is the most suitable by benchmarking how well the different solutions perform. Experiments can be conducted in the living labs. In order to get data, these experiments needs to be performed as soon as possible. 

# Project: Investigate the world of time serie prediction to predict energy flows (2019 - 2020)
The goal of this project is to get a time serie database that accepts (real-)time serie data sources. Within a dashboard the time serie signals together with the prediction of these data sources in time. Furthermore, the dashboard should show how well the prediction performs to predict the data source. It should be possible to add new data sources and add prediction to these data sources.

## Background
The research group Expertise centre of Technical Innovation, Within Avans University of Applied Science, performs research in the field of the energy transition. SmartGrid AI applies machine learning to improve the energy management of a smart grid. With the goal to become fully energy neutral. Within Avans University of Applied Sciences the goal is to become energy neutral. This year all results will be applied to improve the energy management of the laboraty SENDLAB. One room that we would like to make energy neutral.

## Problem statement
Due to the complexity of a smart grid (in a building, campus or room), becoming energy neutral is a difficult (control) task. A lot of uncertainty and system limiations needs to be taken into account. Another aspect is the variety and multiple components that produces and consumes energy. Last project, students have applied deep reinforcement learning (DRL). The algoritm showed that it was able to learn and improve during time. Unfortunately, it has not yet leaded to significant improvement of the energy management of the smart grid.

The algorithm could be improved when the algorithm also get a prediction of the production and consumption of the energy flows within the smart grid. Preduction of time serie data is not yet researched within SmartGrid AI.

# Project: Apply deep reinforcement learning (DRL) to control a smart grid (2018 - 2019)
 Students have been working on deep reinforcement learning (DRL). Such algorithm is able to control a smart grid, like batteries and dishwashers for example. It has been shown that DRL could be used to control a smart grid at home. However, the DRL algorithm showed learning, but it was still not performing quite well.

Improvement of these algorithm, could be found in the prediction of the datasource that are used by these algorithms. This project is about how artificial intelligence can be applied to predict time serie signals. Time serie data sources that need to be predicted are solar panels and consumption of energy.


