# Time serie prediction

SmartGrid AI is a research area that applies artificial intelligence within the context of the energy transition. Students have been working on deep reinforcement learning (DRL). Such algorithm is able to control a smart grid, like batteries and dishwashers for example. It has been shown that DRL could be used to control a smart grid at home. However, the DRL algorithm showed learning, but it was still not performing quite well.

Improvement of these algorithm, could be found in the prediction of the datasource that are used by these algorithms. This project is about how artificial intelligence can be applied to predict time serie signals. Time serie data sources that need to be predicted are solar panels and consumption of energy.

The goal of this project is to get a time serie database that accepts (real-)time serie data sources. Within a dashboard the time serie signals together with the prediction of these data sources in time. Furthermore, the dashboard should show how well the prediction performs to predict the data source. It should be possible to add new data sources and add prediction to these data sources.
# Background
The research group Expertise centre of Technical Innovation, Within Avans University of Applied Science, performs research in the field of the energy transition. SmartGrid AI applies machine learning to improve the energy management of a smart grid. With the goal to become fully energy neutral. Within Avans University of Applied Sciences the goal is to become energy neutral. This year all results will be applied to improve the energy management of the laboraty SENDLAB. One room that we would like to make energy neutral.

# Problem statement
Due to the complexity of a smart grid (in a building, campus or room), becoming energy neutral is a difficult (control) task. A lot of uncertainty and system limiations needs to be taken into account. Another aspect is the variety and multiple components that produces and consumes energy. Last project, students have applied deep reinforcement learning (DRL). The algoritm showed that it was able to learn and improve during time. Unfortunately, it has not yet leaded to significant improvement of the energy management of the smart grid.

The algorithm could be improved when the algorithm also get a prediction of the production and consumption of the energy flows within the smart grid. Preduction of time serie data is not yet researched within SmartGrid AI.
# Research
Research is finding answers to the questions. Therefore, this project has defined a main research question: 

_**How could we apply machine learning to succesfully predict the (real-time) energy production and consumption of a smart grid?**_

This questions gives a clear idea what will be research. In order to give focus sub questions have been defined:
1.	Which two machine learning algorithms could be used best to predict time serie data?
2.	What are the requirements of the dashboard?
3.	How could we perform multiple predictions for multiple data sources?
4.	How could we show time serie data and their prediction on the dashboard?
5.	How could show the performance of a particular prediction?
7.	How could we add and remove data sources of the dashboard?
8.	How could we add and remove predictions on data sources of the dashboard?
# Goal
The goal is to predict all the time serie data sources of the SENDLAB. This data and the prediction will be displayed in a dashboard. It should be possible to easily add and remove data sources. Furthermore, it should be possible to easily add and remove predictions for data sources. Each prediction will also maintain a performance indicator, indicating how well the prediction performs. It should be possible to implement different prediction algorithms.

# Approach
The following activities will be executed in weekly sprints:
1. Desk research "Which machine learning algorithms could be used to predict time serie data sources?" and "How could we compare the found machine learning algorithms?". Resulting into a comparison of machine learning algorithms and the selection of the two best algorithms that will taken in the next activity.
2. Defining the requirements and global design of the dashboard.
3. Experiment machine learning algorithm. Based on a time serie data source, the students are experimenting to perform prediction of the time serie data source with the first and second algorithm.
4. Development of the dashboard.
