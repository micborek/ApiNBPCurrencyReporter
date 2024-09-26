import re
import logging
from datetime import datetime

from constants import (
    ALLOWED_CURRENCY_CODES,
    ALLOWED_DATE_PATTERN
)

logger = logging.getLogger(__name__)


def validate_parameters(currencies: dict, budget: float, start_date: str, days_number: int):
    """Main function for running validation checks on input parameters for Report class instance"""

    check_if_shares_allowed(currencies)
    check_if_correct_budget(budget)
    for currency_code in currencies:
        check_if_currency_allowed(currency_code)
    check_if_date_format_allowed(start_date)
    check_if_days_number_correct(days_number)


def check_if_shares_allowed(currencies_input: dict):
    """Check if requested currencies shares sum up to 100 percent"""
    sum_checked = 0
    for share in currencies_input.values():
        sum_checked += share
    if sum_checked != 100:
        logger.exception(f'{currencies_input} currency shares do not sum up to 100 percent.')
        raise ValueError


def check_if_currency_allowed(currency_code: str):
    """Check if requested currency is in allowed currency list"""
    if currency_code.upper() not in ALLOWED_CURRENCY_CODES:
        logger.exception(f'{currency_code.upper()} currency code is not allowed.')
        raise ValueError


def check_if_date_format_allowed(date: str):
    """Check if date string is in an expected format"""
    if not re.match(ALLOWED_DATE_PATTERN, date):
        logger.exception(f'{date} format is not allowed. Please use YYYY-MM-DD.')
        raise ValueError


def check_if_end_date_correct(end_date):
    """Check if end date is already in the past"""
    if not end_date < datetime.now():
        logger.exception(f'{end_date} is not allowed. Report generation works only for the past.')
        raise ValueError


def check_if_correct_budget(initial_budget: float):
    """Check if requested budget is greater than zero"""
    if initial_budget < 0:
        logger.exception(f'Initial budget needs to be greater than zero.')
        raise ValueError


def check_if_days_number_correct(days_number: int):
    """Check if request period in days is an integer value"""
    if not isinstance(days_number, int):
        logger.exception("Report's day period needs to be an integer.")
        raise TypeError
