from helpers import (
    calculate_days_time_delta,
    get_currency_rates_from_api,
    calculate_report_data, calculate_total_value
)
from validators import validate_parameters

import logging

logger = logging.getLogger(__name__)


class Report:
    """Class representing a report"""

    def __init__(self, requested_currencies, initial_budget, start_date, report_days_period):
        """Constructs all the necessary attributes for the report object."""

        self.requested_currencies = requested_currencies
        self.initial_budget = initial_budget
        self.start_date = start_date
        self.report_days_period = report_days_period
        self.end_date = ''
        self.api_currencies_data = []
        self.currencies_data_in_pln = {}
        self.currencies_total_value = {}

    def generate_report(self):
        """Main method for report generation. Uses attributes defined as input parameters and modifies them"""

        try:
            # validate input parameters
            validate_parameters(currencies=self.requested_currencies, budget=self.initial_budget,
                                start_date=self.start_date, days_number=self.report_days_period)

            # calculate end date of the report
            self.end_date = calculate_days_time_delta(self.start_date, self.report_days_period)

            # get needed currency rates from API
            for currency, share in self.requested_currencies.items():
                api_data = get_currency_rates_from_api(currency_code=currency, start_date=self.start_date,
                                                       end_date=self.end_date)
                self.api_currencies_data.append(api_data.json())

            # calculate value of bought currencies in a given time period in PLN
            self.currencies_data_in_pln = calculate_report_data(self.api_currencies_data, self.requested_currencies,
                                                                self.initial_budget)

            # calculate full value of bought currencies
            self.currencies_total_value = calculate_total_value(self.currencies_data_in_pln)

        except BaseException as e:
            logger.exception(f"An exception occurred when processing : {e}")
