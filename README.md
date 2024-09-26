# ApiNBPCurrencyReporter
Utilize the API provided by the National Bank of Poland (NBP) to calculate and visualize the value of a currency investment over a specified period. Users can select different currencies, specify their share in the investment, define an initial budget in PLN, and choose a time period (in days) for which the investment's value will be calculated and displayed.

The application is built using core Python, with the requests library for API calls and matplotlib for data visualization.

It can be enhanced with refactoring and the addition of unit tests in the future.

## Running
The app was written in Python 3.12 and can be run by executing the main.py file after installing the required modules listed in requirements.txt. The desired output should be specified in input_parameters.py.

# Example of a report run
The results of an exemplary run are presented below, based on the following input parameters:
* Initial budget - 1000 PLN
* Currencies to be bought and their share in initial budget - USD 30%, EUR 40%, HUF 30%
* Start date - 2024-06-04
* Period to be checked in days - 30

Created charts may be seen below.

## Initial shares in bought currencies - as defined in input parameters
![Figure1](/visualization_examples/initial_share.png)

## USD bought for 300 PLN - value change in a time period
![Figure3](/visualization_examples/usd_value.png)

## EUR bought for 400 PLN - value change in a time period
![Figure3](/visualization_examples/eur_value.png)

## HUF bought for 300 PLN - value change in a time period
![Figure3](/visualization_examples/huf_value.png)

## Total of bought currencies for 1000 PLN - value change in a time period
![Figure3](/visualization_examples/total_value.png)

## Final shares in bought currencies - as calculated with currency rates in a time period
![Figure2](/visualization_examples/end_share.png)

