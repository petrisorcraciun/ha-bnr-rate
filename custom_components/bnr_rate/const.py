from datetime import timedelta

DOMAIN = "bnr_rate"
BNR_API_URL = "https://www.bnr.ro/nbrfxrates.xml"
BNR_XML_NAMESPACE = "http://www.bnr.ro/xsd"

DEFAULT_NAME = "BNR Rate"
DEFAULT_CURRENCY = "RON"
DEFAULT_MULTIPLIER = 1

AVAILABLE_CURRENCIES = [
    "EUR",
    "USD",
    "GBP"
]

BNR_UPDATE_HOUR = 13
BNR_UPDATE_MINUTE = 5

BNR_MAX_RETRIES = 3 
BNR_RETRY_INTERVAL = 300
BNR_SKIP_WEEKDAYS = [5, 6]
