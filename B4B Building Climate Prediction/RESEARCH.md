# Transformer research

- encoder/decoder: stack of LSTM's or GRU's. Encoders collect information on element it recieves and propegates it forward. The data is then moved through the encoder vector, where it encapsulates the information for the decoders. decoders predict an output from the info the encoders propagated forward. 

    ![](data:image/png;base64,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)
- Attention mechanism: Instead of encoding the entire sentence in a hidden state, with attention, we give every word a hiddenstate and pass it onto the decoder. here the decoder uses each hidden state to decode the data. Why would you do this? the idea behind the attention mechanism is that every datapoint can have valueable information. so in order for the decoding to be precise, it needs to take every dat point into account.

- Cnn layer: The cnn layers give the Transformer model the posibility to process the datapoints in paralel. at the same time the "distance" between datapoints stays very small, which means attention can be retained across a large number of datapoints.

- Self attention: A specific attention mechanisms applied on transformers. The Inputs in the self-attention module are allowed to interact with eachother and figure out what input requires the most attention. the outputs are grouped into clusters of these interaction and attention scores. This is done by

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
