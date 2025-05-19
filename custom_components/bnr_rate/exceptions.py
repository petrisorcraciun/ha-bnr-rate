class BNRRateError(Exception):
    pass

class BNRRateConnectionError(BNRRateError):
    pass

class BNRRateParseError(BNRRateError):
    pass

class BNRRateCurrencyError(BNRRateError):
    pass
