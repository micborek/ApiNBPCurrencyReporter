from input_parameters import (
    requested_currencies_input,
    initial_budget_input,
    start_date_input,
    report_days_period,
    log_level
)
from helpers import (
    print_full_report,
    print_report_conclusions
)
from Reporter import Report
from Visualizer import Visualizer

import logging

logger = logging.getLogger(__name__)
logging.basicConfig(level=log_level)

if __name__ == "__main__":
    # Report data generation
    logger.info("Report generation started.")
    report = Report(requested_currencies_input, initial_budget_input, start_date_input, report_days_period)
    report.generate_report()
    logger.info('Generation of report data finished. Printing results.')
    logger.debug(print_full_report(report.currencies_data_in_pln))
    print_report_conclusions(report.currencies_data_in_pln)

    # Report visualization
    visualizer = Visualizer(report.currencies_data_in_pln, requested_currencies_input, report.currencies_total_value)
    visualizer.visualize_report_data()
    logger.info("Report generation and visualisation finished.")
