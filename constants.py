# this file stores constants needed for the app flow
API_NBP = "https://api.nbp.pl/api/exchangerates/rates/{table_type}/{currency_code}/{start_date}/{end_date}/?format=json"
API_DATE_FORMAT = "%Y-%m-%d"
ALLOWED_CURRENCY_CODES = ['USD', 'EUR', 'HUF']
ALLOWED_DATE_PATTERN = "^\d{4}-\d{2}-\d{2}$"

# dictionary keys
PLN_VALUES_KEY = 'value_in_pln'
CUR_VALUES_KEY = 'value_in_currency'
EFF_DATE_KEY = 'effective_date'
RATE_KEY = 'rate'

# API dictionary keys
MID = 'mid'
RATES = 'rates'
CURRENCY_CODE = 'code'
EFF_DATE_API_KEY = 'effectiveDate'