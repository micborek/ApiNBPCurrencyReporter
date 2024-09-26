from helpers import (
    visualize_currency_worth_data,
    visualize_initial_budget_shares,
    visualize_end_budget_shares,
    visualize_currency_total_worth
)

import logging

logger = logging.getLogger(__name__)


class Visualizer:
    """Class for visualizing report's data"""

    def __init__(self, report_data, initial_budget_data, total_value):
        """Constructs all the necessary attributes for the visualization object."""

        self.report_data = report_data
        self.initial_budget_data = initial_budget_data
        self.total_value = total_value

    def visualize_report_data(self):
        """Main method for data visualization"""

        try:
            visualize_initial_budget_shares(self.initial_budget_data)
            visualize_end_budget_shares(self.report_data)
            visualize_currency_worth_data(self.report_data)
            visualize_currency_total_worth(self.total_value)

        except BaseException as e:
            logger.exception(f"An exception occurred when processing : {e}")
