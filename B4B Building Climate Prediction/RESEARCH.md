# Temporal Fusion Transformer (TFT)

## Introduction

The objective of the B4B climate prediction team is to build/find and train a machine learning model that can predict the internal climate of a building. An important factor in this equation is time, since time is intertwined with a lot of variables like the amount of people that are in the building at any given time, or the seasons and thus the outside temprature. Thus Timeseries data has to be used to make acurate predictions of the future state of the building climate. Our predecessors tried to do this with the help of LSTM's, but have been unsucessfull in producing an acurate prediction model. After researching subquestion number 5 (Which ML algorithms should be used to perform prediction of these timeseries measurements?) Our team came across the Temporal Fusion Transformer. After a few test runs with the model we managed to create a good prediction model that could acurately predicit future timesteps, but the inner workings of this model were still unknown. This begs the following question: What is a TFT model, and how does it predict future Timesteps?

For the forcast predictions we used a (at this time) state of the art model specifically build for TimeSeries predicitions, The Temporal Fusion Transformer. The TFT specializes on Multi-Horizon forcasting (a model capable of predicting multiple attributes at once) which is needed for the predicting a climate within a building, since the climate is defined by more than one variable. In this document, we will shortly discuss the architecture of this model. This document is not a replacement for the TFT paper. Please read and research the sources given if you require a full understanding of this model and how it operates.

Below you can see the architecture of the TFT, with an explanation on how it works just below it.

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
