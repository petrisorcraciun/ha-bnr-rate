# ha-bnr-rate
Home Assistant custom component for fetching and displaying the official exchange rates from the National Bank of Romania (BNR)

**Romanian version available:** [README.ro.md](./README.ro.md)

## Features
- Sensor for each supported currency (e.g., EUR, USD, GBP)
- Automatic update at the BNR publishing hour (default 13:05)
- Shows full currency name, multiplier, and last update time
- Skips requests on weekends (Saturday and Sunday)

## Installation

### Manual Installation
1. Copy the `bnr_rate` folder into your Home Assistant `custom_components` directory.
2. Restart Home Assistant.
3. Go to **Settings → Devices & Services → Add Integration** and search for **BNR Rate** to add and configure the integration from the UI.

### HACS Installation

[![Add Integration in Home Assistant](https://my.home-assistant.io/badges/config_flow_start.svg)](https://my.home-assistant.io/redirect/hacs_repository/?owner=petrisorcraciun&repository=ha-bnr-rate&category=integration)

1. In Home Assistant, go to **HACS → Integrations → Custom repositories**.
2. Add this repository (`https://github.com/petrisorcraciun/ha-bnr-rate`) as a custom integration.
3. Search for **BNR Rate** in HACS and install it.
4. Restart Home Assistant.
5. Go to **Settings → Devices & Services → Add Integration** and search for **BNR Rate** to add and configure the integration from the UI.

> **Note:** You can add or remove supported currencies by editing the `AVAILABLE_CURRENCIES` list in `const.py`.

## Exposed Attributes
- `publishing_date`: Date of the published rate
- `currency_name`: Full name of the currency
- `multiplier`: Multiplier (e.g., 1, 10, 100)
- `last_success_update`: Date/time of the last successful update

## Dependencies

This integration does **not** use or require any additional Python libraries. All dependencies are already included in Home Assistant by default.

## Data Source

The exchange rates are fetched directly from the official National Bank of Romania (BNR) XML feed.

## About `const.py`

The `const.py` file contains all the main constants used by the integration. You can customize the integration's behavior by editing this file:

- `DOMAIN`: The domain name for the integration (should not be changed).
- `BNR_API_URL`: The URL for the BNR XML feed.
- `BNR_XML_NAMESPACE`: The XML namespace used for parsing the BNR XML.
- `CONF_CURRENCY`, `DEFAULT_NAME`, `DEFAULT_CURRENCY`, `DEFAULT_MULTIPLIER`: Configuration defaults.
- `MIN_TIME_BETWEEN_UPDATES`: Minimum interval between updates (as a `timedelta`).
- `AVAILABLE_CURRENCIES`: List of supported currencies. You can add or remove currencies here (must match the codes in the BNR XML).
- `BNR_UPDATE_HOUR`, `BNR_UPDATE_MINUTE`: The hour and minute when BNR usually publishes new rates (used for scheduled updates).
- `BNR_MAX_RETRIES`: How many times to retry fetching data if the request fails.
- `BNR_RETRY_INTERVAL`: How many seconds to wait between retries (e.g., 300 for 5 minutes).
- `BNR_SKIP_WEEKDAYS`: List of weekdays (Python: Monday=0, Sunday=6) when requests should be skipped (default: [5, 6] for Saturday and Sunday).

> **Tip:** If you add a new currency code to `AVAILABLE_CURRENCIES`, also add its full name in `currency_names.py` for a better display in Home Assistant.

## Support
- [GitHub](https://github.com/petrisorcraciun/ha-bnr-rate)

---
**Author:** [petrisorcraciun](https://github.com/petrisorcraciun)


<a href="https://www.buymeacoffee.com/petrisorcraciun"><img src="https://img.buymeacoffee.com/button-api/?text=Buy me a coffee&emoji=&slug=petrisorcraciun&button_colour=FFDD00&font_colour=000000&font_family=Poppins&outline_colour=000000&coffee_colour=ffffff" /></a>
