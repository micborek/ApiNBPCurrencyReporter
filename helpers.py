import datetime
import logging
import requests
import json
import matplotlib.pyplot as plt

from constants import (
    API_NBP,
    API_DATE_FORMAT,
    PLN_VALUES_KEY,
    EFF_DATE_KEY,
    CUR_VALUES_KEY,
    MID, RATE_KEY,
    RATES,
    CURRENCY_CODE,
    EFF_DATE_API_KEY
)
from validators import check_if_end_date_correct

# disable unnecessary logging for matplotlib
mpl_logger = logging.getLogger('matplotlib')
mpl_logger.setLevel(logging.ERROR)
pil_logger = logging.getLogger('PIL')
pil_logger.setLevel(logging.ERROR)

logger = logging.getLogger(__name__)


def calculate_days_time_delta(start_date: str, report_days_period: int) -> str:
    """Calculate the report's end date based on start date and report days period,
    validate if calculated end date is in the past"""

    start_date_object = datetime.datetime.strptime(start_date, API_DATE_FORMAT)
    end_date_object = start_date_object + datetime.timedelta(days=report_days_period)
    end_date = end_date_object.strftime(API_DATE_FORMAT)
    logger.info(f"Start date requested- {start_date} - End data calculated - {end_date}")
    check_if_end_date_correct(end_date_object)
    return end_date


def get_currency_rates_from_api(currency_code: str, start_date: str, end_date: str, table_type='a'):
    """Make a call to API for currency rates in a given period. Default API table type set to 'a'"""

    currency_data = requests.get(
        API_NBP.format(table_type=table_type, currency_code=currency_code, start_date=start_date,
                       end_date=end_date))
    logger.info(f"Data for {currency_code.upper()} obtained successfully.")
    return currency_data


def calculate_report_data(api_currencies_data: list, requested_currencies, initial_budget) -> dict:
    """Calculate the report's results. For each currency calculate its start value and values in following dates
    until the end date"""

    # results placeholder for all currencies
    api_currencies_data_in_pln = {}

    for currency_rates in api_currencies_data:
        currency_code = currency_rates[CURRENCY_CODE]
        pln_initial_budget = requested_currencies[currency_code] * initial_budget * 0.01
        rates = currency_rates[RATES]

        logger.debug(
            f'Calculating worth of {currency_code.upper()} currency in {pln_initial_budget} PLN in a given period.')

        # results placeholder for the processed currency
        dicts_list = []
        for index, rate_info in enumerate(rates):
            # first iteration - calculate start value
            if not index:
                worth_in_pln = {EFF_DATE_KEY: rate_info[EFF_DATE_API_KEY],
                                CUR_VALUES_KEY: pln_initial_budget / rate_info[MID],
                                PLN_VALUES_KEY: pln_initial_budget,
                                RATE_KEY: rate_info[MID]}

                currency_initial_budget = pln_initial_budget / rate_info[MID]
            else:
                worth_in_pln = {EFF_DATE_KEY: rate_info[EFF_DATE_API_KEY],
                                CUR_VALUES_KEY: currency_initial_budget,
                                PLN_VALUES_KEY: currency_initial_budget * rate_info[MID],
                                RATE_KEY: rate_info[MID]}

            dicts_list.append(worth_in_pln)
            api_currencies_data_in_pln[currency_code] = dicts_list

    return api_currencies_data_in_pln


def print_full_report(report_data: dict):
    """Print full report as pretty-print json"""

    return json.dumps(report_data, indent=2)


def print_report_conclusions(report_data: dict):
    """Print short summary of the generated report - show currencies value at the beginning and at the end"""

    for currency_code, currency_data in report_data.items():
        start_data = currency_data[0]
        start_value = start_data[PLN_VALUES_KEY]
        end_data = currency_data[-1]
        end_value = end_data[PLN_VALUES_KEY]
        logger.info(f"{currency_code} start value - {start_value}, end value - {end_value}")


def visualize_currency_worth_data(report_data):
    """Display a line chart for each currency and its worth in time period
    This one should be re-factored to not repeat code with visualize_currency_total_worth"""

    # process data for each currency in the report
    for currency_code, currency_data in report_data.items():
        currency_values = []
        currency_dates = []
        # prepare values for chart plot
        for data_piece in currency_data:
            currency_values.append(data_piece.get(PLN_VALUES_KEY))
            currency_dates.append(data_piece.get(EFF_DATE_KEY))

        # adjust plot size, so it is more readable
        plt.figure().set_figwidth(15)
        # add value labels to chart markers
        for i, value in enumerate(currency_values):
            plt.text(i, value + 0.1, str(round(float(value), 2)), ha='center')

        plt.plot(currency_dates, currency_values, marker='o')
        plt.title(f"{currency_code} - bought value change in PLN")
        plt.xticks(rotation=45)
        plt.ylabel("Value in PLN")
        plt.xlabel("Effective Date")
        plt.show()


def visualize_currency_total_worth(total_worth_data):
    """Display a line chart for each currency and its worth in time period.
    This one should be re-factored to not repeat code with visualize_currency_worth_data"""

    currency_values = []
    currency_dates = []
    # prepare values for chart plot
    for effective_date, value in total_worth_data.items():
        currency_values.append(value)
        currency_dates.append(effective_date)

    # adjust plot size, so it is more readable
    plt.figure().set_figwidth(15)
    # add value labels to chart markers
    for i, value in enumerate(currency_values):
        plt.text(i, value + 0.1, str(round(float(value), 2)), ha='center')

    plt.plot(currency_dates, currency_values, marker='o')
    plt.title(f"Total bought value change in PLN")
    plt.xticks(rotation=45)
    plt.ylabel("Value in PLN")
    plt.xlabel("Effective Date")
    plt.show()


def visualize_initial_budget_shares(initial_budget_data):
    """Display a pie chart for initial budget shares in currencies
    A function for pie-chart generation should be created to not repeat code in visualize_end_budget_shares"""

    # prepare values for chart plot
    currency_codes = []
    currency_shares = []
    for currency_code, currency_share in initial_budget_data.items():
        currency_codes.append(currency_code)
        currency_shares.append(currency_share)

    # plot pie chart with percent values displayed
    fig, ax = plt.subplots()
    ax.pie(currency_shares, labels=currency_codes, autopct='%1.1f%%')
    plt.title(f"Initial value shares in currencies")
    plt.show()


def visualize_end_budget_shares(report_data):
    """Display a pie chart for final budget shares in currencies
    A function for pie-chart generation should be created to not repeat code in visualize_initial_budget_shares"""

    # prepare values for chart plot
    currency_codes = []
    currency_shares = []
    for currency_code, currency_data in report_data.items():
        currency_codes.append(currency_code)
        currency_shares.append(currency_data[-1].get(PLN_VALUES_KEY))

    # plot pie chart with percent values displayed
    fig, ax = plt.subplots()
    ax.pie(currency_shares, labels=currency_codes, autopct='%1.1f%%')
    plt.title(f"End value shares in currencies")
    plt.show()


def calculate_total_value(report_data: dict) -> dict:
    """Use calculated currency values to get their total value"""

    total_values = {}
    for currency_code, currency_data in report_data.items():
        for data in currency_data:
            if not total_values.get(data[EFF_DATE_KEY]):
                total_values[data[EFF_DATE_KEY]] = data[PLN_VALUES_KEY]
            else:
                total_values[data[EFF_DATE_KEY]] = data[PLN_VALUES_KEY] + total_values[data[EFF_DATE_KEY]]

    return total_values
