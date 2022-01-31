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

# Our Answer
The main question our team had to answer was the following: __“How could we predict future measurements concerning the internal climate of a building that can be used by the building automation controller and independently as prediction.”__

To answer this question, a set of subquestions were formulated:
1.	What are the most important measurement that need to be predicted of the internal climate of a building?
2.	How should the prediction look like?
3.	Which datasets can be used to train, validate and test the algorithms?
4.	What kind of interface should be defined to integrate the software algorithm with the building automation controller?
5.	Which ML algorithms should be used to perform prediction of these timeseries measurements?
6.	How should the software be setup that it is user friendly and can be used by technical people with limited AI knowledge?

After a period of 10 weeks working on the project, we we're able to answer 5 of the 6 subquestions:

1. After discussing this question with our mentor, we concluded that these 3 measurements are the most important to predict when it comes to an internal climate: Temprature, Humidity and CO2 values (Or the overal air composition). These being the 3 main factors which determine if the climate is percieved as "pleasant" or not by the visitors of the building. 
2. Since we are working with a TimeSeries, the predicitons should look like a signal. At a certain amount of time intervals in the future, which the model is trained with, there should be a prediction of temprature, humidity and CO2 percentage in the air. This will give the controller the ability to adjust the indoor climate based on the predicitons made.
3. The current datasets we have used for internal climates all contained the target (temp, humidity, CO2) values. There we're a lot of datasets, and we haven't managed to boil it down to a dataset that is 'best'. To resolve this problem, we have made our model as modular as possible by taking a script approach and something of an 'open ai gym enviroment' approach with our model class. See the manual and scripts for more info.
4. Unfortunately we haven't had the time to research this, so we do not have an answer to this question
5. We have used the Temporal Fusion Transformer model, which we think is currently the best model for TimeSeries prediction out there. See the rest of the research.md file for a deep dive into the Temporal Fusion Transformer
6. We have setup multiple python scripts with a explanitory guide on how to setup your device to use these scripts. This way a technical person with limited AI knowledge can train his/her own model with different datasets if need be.
    1. A generate csv script, to clean up and ready the dataset for usage.
    2. A generate model config script, to create a config used to generate and train a model. This config can be adjusted before training. If need be you can adjust hyperparameters and other settings here.
    3. A train script to train an actual modal. If you have specified it in the generate script, the train script can do automatic hyperparameter tuning.
    4. A predict script. The predict script returns a csv with predicted values in future timestamps in a csv (how many is dependent on your cfg file).

Now that the subquestions have been answered we can answer the main question: __“How could we predict future measurements concerning the internal climate of a building that can be used by the building automation controller and independently as prediction.”__

Future measurements concerning the internal climate of a building can be predicted by a Temporal Fusion Transformer model that outputs a list of predictions, which can then be used by a building automation controller or independently.

<br/><br/>
# Temporal Fusion Transformer (TFT)

## Introduction

Now we know what the project is all about, and what the project team has acomplished, we can explain what the Temporal Fusion Transformer is. An important factor in the equation is time, since time is intertwined with a lot of variables like the amount of people that are in the building at any given time, or the seasons and thus the outside temprature. Thus Timeseries data has to be used to make acurate predictions of the future state of the building climate. Our predecessors tried to do this with the help of LSTM's, but have been unsucessfull in producing an acurate prediction model. After researching subquestion number 5 (Which ML algorithms should be used to perform prediction of these timeseries measurements?) Our team came across the Temporal Fusion Transformer. After a few test runs with the model we managed to create a good prediction model that could acurately predicit future timesteps, but the inner workings of this model were still unknown. This begs the following question: What is a TFT model, and how does it predict future Timesteps? 

In short, The TFT specializes on Multi-Horizon forcasting (a model capable of predicting multiple attributes at once) which is needed for the predicting a climate within a building, since the climate is defined by more than one variable. Next to that it uses self-attention to take learn the temporal relationship of variables or targets within a Timeseries dataset. In this document, we will shortly discuss the architecture of this model. This document is not a replacement for the TFT paper. Please read and research the sources given if you require a full understanding of this model and how it operates.

Below you can see the architecture of the TFT, with an explanation following shortly after it.

![](Img\Model_Architecture_tft.PNG)

The model can be divided into 5 layers:

1. Variable selection networks
2. Static covariate encoders
3. Gating mechanisms
4. Temporal proces
5. Prediction intervals

## 1. Variable selection networks

By implementing variable selection networks, the TFT can select the most impactfull variables and also remove any unnecessary noisy inputs which can negatively impact preformance. It does this for both categorical and continious variables. For categorical values entity embeddings are used as feature representations, for continious variables linear transformations are applied. Each input variable is transformed into a vector that fits the input and subsequent dimensions of the network for skip connections. 

## 2. Static covariate encoders

In contrast with other time series forecasting architectures, the TFT is carefully designed to integrate information from static metadata, using separate GRN encoders to produce four different context vectors, $c_{s}, c_{e}, c_{c},$ and $c_{h}$. These contect vectors are wired into various locations in the temporal fusion decoder where static variables play an important role in processing. Specifically, this includes contexts for (1) temporal variable selection $(c_{s})$, (2) local processing of temporal features $(c_{c}, c_{h})$, and (3) enriching of temporal features with static information $(c_{e})$. As an example, taking $ζ$ to be the output of the static variable selection network, contexts for temporal variable selection would be encoded according to $c_{s} = GRN_{c_{s}}(ζ)$. Exact details of these implementations are coverd in the Temporal proces section.

## 3. Gating mechanisms

![](Img\GRN.PNG)

*Figure 3, Gated Residual Network (GRN)*

Because precise relationships between exogenous inputs and target variables is often unknown in advance and determining if non-linear processing is required, the TFT model makes use of GRN's (Gated Residual Network). These GRN's take in a primary input and an optional context. By utilizing an ELU (Exponential Linear Unit) activation function, it can provide us with either an identity function ( if $ELU(a)$ where $a >> 0$) or a constant output in linear behavior (if $ELU(a)$ where $a << 0$). Another important aspect of the GRN is the GLU (Gated Linear Unit) which is the gate in figure 3. The GLU lets the TFT control to which extent the GRN contributes to the original input, potentially skipping over the entire layer if necessary as the outcome of the GLU could be close to 0 to supress the non-linear contribution.

## 4. Temporal proces & IMHA

### 4.1 Interpretable Multi-Head attention (IMHA)

The TFT makes use of a modified Attention mechanism, which was first introduced in regular transformer networks. To understand this modified version we must first cover regular and multiheaded attention. In principle, the input for the attention mechanism is converted to a Query ($Q$) Key ($K$) and Value ($V$) vector. $Q$ and $K$ are pulled through a normilazation operation, often the scaled dot-product attention:($Softmax(QK^{T}/ \sqrt {d_{attn}})$) (source 1). An improvement on the attention mechanism is the multiheaded attention (source 1). By using different heads, the model can encode multiple relationships and nuances for each input. This greatly improves the learning ability of the model. I've included 4 sources under the self attention paper which go in to great detail on how the attention mechanisms work if further explanation is needed. To make the model more explainable, Interpretable multiheaded attention is used. By sharing weights and values across all heads, the IMHA yields an increased representation capacity, compared to the regular multi-headed attention.

### 4.2 Temporal process (Temporal Fusion Decoder)

This is where the 'magic' happens. There are multiple layers in the Temporal Fusion Decoder (TFD) to learn temporal relationships present in data.

#### 4.2.1 Locality Enhancement with Sequence-to-Sequence Layer

In time series data, important data points are often identified by the relation they have with the surounding values. For example: anomalies, change-points or cyclical patterns. By leveraging local context (through feature construction that utilizes pattern info on top of point-wise values) it is possible to achieve preformance improvements in attention-based architecture. The way the TFT does this is by uitilizing a sequence to sequence model. This generates a set of uniform temporal features which serve as inputs into the temporal fusion decoder itself. 

#### 4.2.2 Static Enrichment Layer

Static covariates often have a significant influence on the temporal dynamics (e.g. genetic information on disease risk). To account for this, the TFD makes use of a static enrichment layer which enhances the temporal features with static metadata. For this operation, a GRN is used where the aforementioned context vector $c_{e}$ is used for the enrichment, which comes from a static covariate encoder in the 2nd layer of the TFT model.

#### 4.2.3 Temporal Self-Attention Layer

After the enrichment, self attention with IMHA is applied. decoder masking is applied to the multi-head attention layer to ensure that each temporal dimension can only attend to features preceding it. Besides preserving causal information flow via masking, the self-attention layer allows TFT to pick up long-range dependencies that may be challenging for RNN-based architectures to learn. Following the self-attention layer, an additional gating layer is also applied to facilitate training

#### 4.2.4 Position-wise Feed-forward Layer

We apply an additional non-linear processing to the outputs of the selfattention layer. Similar to the static enrichment layer, this makes use of  GRNs: $ψ(t, n) = GRN_{ψ} (δ(t, n))$ where the weights of $GRN_{ψ}$ are shared across the entire layer. As per Fig. 2, we also apply a gated residual connection which skips over the entire transformer block, providing a direct path to the sequence-to-sequence layer – yielding a
simpler model if additional complexity is not required, as shown here: $\widetilde{ψ}(t, n) = LayerNorm(\widetilde{φ}(t, n) + GLU\widetilde{ψ}(ψ(t, n)))$

#### 4.2.5 Quantile outputs

The TFT predicts intervals on top of point forecasts, by prediciting various percentiles simultaneously at a given time step. These forecasts are only generated for horizons in the future. 

## 5. Loss function

Before we explain the loss function of the model, we first need to understand what quantiles are and what quantile regression is.

Quantile: a quantile defines a particular part of a data set. It determines how many values in a distribution are above or below a certain limit. For example, if you have a dataset of 15 points in a linear fasion, a line could be drawn on the 8th point. This line will then be the 50% quantile or the 0.5 quantile (See figure 2). 

![](Img\Capture.PNG)
Figure 2

Quantile regression loss function:
This function is used as the los function for the TFT, and predicts (depending on the input, this could range from 1 to infinity) the quantiles of the target within the timeseries dataset. Where given a prediction $y^{p}_{i}$ and outcome $y_{i}$, the regression loss for a quantile $q$ is:

$L(y^{p}_{i}, y_{i}) = max[q(y_{i} − y^{p}_{i}),  (q − 1)(y_{i} − y^{p}_{i})]$

For a set of predictions, the loss will be the average. 

In the regression loss equation above, as q has a value between 0 and 1, the first term will be positive and dominate when over predicting, $y^{i}_{p} > y_{i}$, and the second term will dominate when under-predicting, $y^{i}_{p} < y_{i}$. For q equal to 0.5, under-prediction and over-prediction will be penalized by the same factor, and the median is obtained. The larger the value of $q$, the more over-predictions are penalized compared to under-predictions. For $q$ equal to 0.75, over-predictions will be penalized by a factor of 0.75, and under-predictions by a factor of 0.25. The model will then try to avoid over-predictions approximately three times as hard as under-predictions, and the 0.75 quantile will be obtained.

TFT is trained by jointly minimizing the quantile loss, summed across all quantile outputs:
$L(Ω,W) = \sum _{{y_{t}∈ Ω }} \sum _{q∈Q} \sum ^{τ_{max}}_{τ=1} \dfrac {QL(yt, yˆ(q, t − τ, τ ), q)}{Mτ_{max}}$
where $Ω$ is the domain of training data containing $M$ samples, $W$ represents the weights of TFT and $Q$ is the set of output quantiles.

## Conclusion

At the beginning of this research document we asked the following question: What is a TFT model, and how does it predict future Timesteps? The TFT model is an attention-based architecture that combines high-performance multi-horizon forecasting with interpretable insights into temporal dynamics. To learn temporal relationships at different scales, TFT uses recurrent layers for local processing and interpretable self-attention layers for long-term dependencies. TFT utilizes specialized components to select relevant features and a series of gating layers to suppress unnecessary components, enabling high performance in a wide range of scenarios.

## Sources: 
- https://arxiv.org/pdf/1706.03762.pdf
    - https://towardsdatascience.com/transformers-explained-visually-part-1-overview-of-functionality-95a6dd460452
    - https://towardsdatascience.com/transformers-explained-visually-part-2-how-it-works-step-by-step-b49fa4a64f34
    - https://towardsdatascience.com/transformers-explained-visually-part-3-multi-head-attention-deep-dive-1c1ff1024853
    - https://towardsdatascience.com/transformers-explained-visually-not-just-how-but-why-they-work-so-well-d840bd61a9d3
- https://towardsdatascience.com/illustrated-self-attention-2d627e33b20a
- https://towardsdatascience.com/transformers-141e32e69591
- https://stats.stackexchange.com/questions/421935/what-exactly-are-keys-queries-and-values-in-attention-mechanisms
- https://www.evergreeninnovations.co/blog-quantile-loss-function-for-machine-learning/
- https://arxiv.org/pdf/1912.09363.pdf
- https://arxiv.org/pdf/2002.07845.pdf
- https://arxiv.org/pdf/1711.11053.pdf
