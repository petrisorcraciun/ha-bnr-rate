"""Exceptions for BNR Rate integration."""

class BNRRateError(Exception):
    """Base exception for BNR Rate integration."""
    pass

class BNRRateConnectionError(BNRRateError):
    """Error occurred while connecting to BNR API."""
    pass

class BNRRateParseError(BNRRateError):
    """Error occurred while parsing BNR API response."""
    pass

class BNRRateCurrencyError(BNRRateError):
    """Error occurred when currency was not found."""
    pass
