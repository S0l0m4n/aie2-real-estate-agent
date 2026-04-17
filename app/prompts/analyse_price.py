# =============================================================================
# System and user prompts for analysing the predicted price using the house
# description and summary stats.
# =============================================================================

ANALYSE_PRICE_PROMPT_SYSTEM = """
## Brief
A machine-language model has predicted the value of a house in Ames, Iowa
according a number of specific features.

## Task
Analyse the predicted house price given the described house features and draw
conclusions based on the summary stats generated from the predicting model's
training data. As one of the house features is the specific neighborhood it's
located in, additional data provided includes a list of the mean sale price ($)
for each possible neighborhood.

## Data
The summary stats and neighborhood mean data are supplied as JSON objects below.
Summary stats include the mean, median, min, max and various quantile values,
plus a count of the training data points.

Summary stats = {summary_stats}

Neighborhood means = {neighborhood_means}

## Extra arguments
The predicted price and list of house features will be supplied by the user.
"""

ANALYSE_PRICE_PROMPT_USER = """
The predicted price is {{price}} dollars for a house with the following
features: {{features}}

Interpret the price against the known statistics and give meaningful insights.
"""
