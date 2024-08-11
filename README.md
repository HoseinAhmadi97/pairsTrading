Dependencies: Numpy; Pandas; Matplotlib and Requests (for fetching TSE price data), Yfinance.

#### - Main Jupyters:
[pairsTrading](/PairsTrading.ipynb) - A simple pairs trading strategy. The signal is given by the ratio of prices on the z score. because the calculation is very long, some output of the calculation is saved in the outputs directory which is used in the next steps in the file.

#### - Secondary Jupyter:
[tse_data_gatherer](data/tse_data_gatherer.ipynb) -
An auxiliary jupyter for pairsTrading which fetches and saves as pickle price data of 550 tse stock symbols.
