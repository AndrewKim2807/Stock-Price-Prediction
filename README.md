<h1 align="center">Stock Price Prediction</h1>
  <h3 align="center">Using an RNN model with LSTM to predict stock prices of the S&P500 index</h3>

</div>

<br/>

<div align="center">
  <a href="#"><img alt="My Github" src="https://img.shields.io/badge/Still%20being%20fixed!-8A2BE2"></a>
  <a href="https://github.com/AndrewKim2807"><img alt="My Github" src="https://img.shields.io/badge/GitHub-%23121011.svg?logo=github&logoColor=white"></a>
  <a href="https://github.com/AndrewKim2807/Stock-Price-Prediction"><img alt="License" src="https://img.shields.io/badge/License-MIT-red"></a>
  <a href="#"><img alt="Visual Studio Code" src="https://img.shields.io/badge/Visual%20Studio%20Code-0078d7.svg?logo=visual-studio-code&logoColor=white"></a>
  <a href="#"><img alt="Python" src="https://img.shields.io/badge/Python-3776AB?logo=python&logoColor=fff"></a>
</div>

<br/>

![Thumbnail](https://github.com/AndrewKim2807/Stock-Price-Prediction/blob/main/Stock%20Price%20Prediction.png)

## Data Prep

The dataset used can be downloaded from [Yahoo Finance ^GSPC](https://finance.yahoo.com/quote/%5EGSPC/history/?p=%5EGSPC&guce_referrer=aHR0cHM6Ly9saWxpYW53ZW5nLmdpdGh1Yi5pby8&guce_referrer_sig=AQAAAHO_ZxM4LqGjzUzgO02Gm4r4zoNEJOBFE_7kGkW6MeuuSyN0pEv_Gg_MduvetWwktnyp7_HUQEbBYmruXnkSjECMVGX8stCFVR4_YOoM-jRoNrm0M9_2KAR_0gEkYoA7ycXjfmwYKTiawCAlAZ-QGmmse90gZDvkwddn4mNmL8Jy). The dataset provides several price points per day.

The Recurrent Neural Network (RNN) is a variant of artificial neural network that incorporates self-connections within its hidden layers, allowing the RNN to leverage past states of its hidden neurons for learning the present state based on new input. RNN demonstrates proficiency in handling sequential data. The Long short-term memory (LSTM) cell serves as a tailored functional component aimed at enhancing RNN's capacity to retain extensive contextual information.

The stock prices is a time series of length $N$, as defined as ${p}_0$, ${p}_1$, $...$, ${p}_N-1$ in which ${p}_i$, is the close price on day $i, 0 <= i <= N$
