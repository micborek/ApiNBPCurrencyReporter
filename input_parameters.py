import logging
# this file stores input parameters for report generation

# currencies chosen for report with their percent share of initial budget (need to sum up to 100)
requested_currencies_input = {'USD': 30, 'EUR': 40, 'HUF': 30}

# initial budget in PLN currency (int/float)
initial_budget_input = 1000

# start date for the report generation in YYYY-MM-DD format (str)
start_date_input = "2024-06-04"

# report period in days (int)
report_days_period = 30

# change log level to INFO to log less
log_level = logging.DEBUG