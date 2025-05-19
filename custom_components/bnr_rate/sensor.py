import logging
from xml.etree import ElementTree as ET
import voluptuous as vol
import aiohttp
from asyncio import sleep
from datetime import datetime
from homeassistant.components.sensor import PLATFORM_SCHEMA, SensorEntity
from homeassistant.const import CONF_NAME
from homeassistant.util import Throttle
from homeassistant.helpers.event import async_track_time_change
from homeassistant.config_entries import ConfigEntry
from homeassistant.core import HomeAssistant

from .const import (
    BNR_API_URL,
    CONF_CURRENCY,
    DEFAULT_NAME,
    DEFAULT_CURRENCY,
    MIN_TIME_BETWEEN_UPDATES,
    AVAILABLE_CURRENCIES,
    BNR_UPDATE_HOUR,
    BNR_UPDATE_MINUTE,
    BNR_MAX_RETRIES,
    BNR_RETRY_INTERVAL,
    DEFAULT_MULTIPLIER,
    BNR_SKIP_WEEKDAYS,
    BNR_XML_NAMESPACE,
)
from .exceptions import BNRRateConnectionError, BNRRateParseError, BNRRateCurrencyError
from .currency_names import CURRENCY_NAMES

_LOGGER = logging.getLogger(__name__)

PLATFORM_SCHEMA = PLATFORM_SCHEMA.extend({
    vol.Optional(CONF_NAME, default=DEFAULT_NAME): str,
    vol.Optional(CONF_CURRENCY, default=DEFAULT_CURRENCY): vol.In(AVAILABLE_CURRENCIES),
})

async def async_setup_platform(hass, config, async_add_entities, discovery_info=None):
    name = config.get(CONF_NAME)
    currency = config.get(CONF_CURRENCY)
    if currency == "all":
        entities = [BNRRateSensor(name, curr) for curr in AVAILABLE_CURRENCIES if curr != "all"]
    else:
        entities = [BNRRateSensor(name, currency)]
    async_add_entities(entities, True)

    for entity in entities:
        async def scheduled_update(now, entity=entity):
            await entity.async_update_ha_state(True)
        async_track_time_change(
            hass,
            scheduled_update,
            hour=BNR_UPDATE_HOUR,
            minute=BNR_UPDATE_MINUTE,
            second=0,
        )

async def async_setup_entry(hass: HomeAssistant, entry: ConfigEntry, async_add_entities):
    name = entry.data.get(CONF_NAME, DEFAULT_NAME)
    currency = entry.data.get(CONF_CURRENCY, DEFAULT_CURRENCY)
    if currency == "all":
        entities = [BNRRateSensor(name, curr) for curr in AVAILABLE_CURRENCIES if curr != "all"]
    else:
        entities = [BNRRateSensor(name, currency)]
    async_add_entities(entities, True)
    for entity in entities:
        async def scheduled_update(now, entity=entity):
            await entity.async_update_ha_state(True)
        async_track_time_change(
            hass,
            scheduled_update,
            hour=BNR_UPDATE_HOUR,
            minute=BNR_UPDATE_MINUTE,
            second=0,
        )

class BNRRateSensor(SensorEntity):
    def __init__(self, name, currency):
        self._name = name
        self._currency = currency
        self._state = None
        self._available = True
        self._publishing_date = None
        self._multiplier = DEFAULT_MULTIPLIER
        self._last_success_update = None
        self._attr_unique_id = f"bnr_rate_{currency.lower()}"

    @property
    def name(self):
        return f"{self._name} {self._currency}"

    @property
    def state(self):
        return self._state

    @property
    def unit_of_measurement(self):
        return DEFAULT_CURRENCY
    
    @property 
    def available(self): 
        return self._available

    @property
    def extra_state_attributes(self):
        attrs = {}
        if self._publishing_date:
            attrs["publishing_date"] = self._publishing_date
            attrs["currency_name"] = CURRENCY_NAMES.get(self._currency, self._currency)
            attrs["multiplier"] = self._multiplier
        if self._last_success_update:
            attrs["last_success_update"] = self._last_success_update.isoformat()
        return attrs

    @Throttle(MIN_TIME_BETWEEN_UPDATES)
    async def async_update(self):
        if datetime.now().weekday() in BNR_SKIP_WEEKDAYS:
            _LOGGER.info("BNRRateSensor: No request on this day (weekend).")
            raise BNRRateConnectionError("BNRRateSensor: No request on this day (weekend).")

        for attempt in range(1, BNR_MAX_RETRIES + 1):
            try:
                _LOGGER.info(f"Requesting BNR rates from {BNR_API_URL}")
                async with aiohttp.ClientSession() as session:
                    try:
                        async with session.get(BNR_API_URL) as response:
                            try:
                                response.raise_for_status()
                            except Exception as error:
                                raise BNRRateConnectionError(f"Connection error: {error}")
                            try:
                                xml_data = await response.text()
                            except Exception as error:
                                raise BNRRateParseError(f"Error reading response: {error}")

                    except aiohttp.ClientError as error:
                        raise BNRRateConnectionError(f"Connection error: {error}")

                try:
                    _LOGGER.warning(f"BNR XML response: {xml_data}")
                    root = ET.fromstring(xml_data)
                    ns = {"bnr": BNR_XML_NAMESPACE}
                except Exception as error:
                    raise BNRRateParseError(f"Failed to parse XML: {error}")

                publishing_date_elem = root.find(".//bnr:PublishingDate", ns)
                if publishing_date_elem is not None:
                    self._publishing_date = publishing_date_elem.text
                else:
                    self._publishing_date = None

                rates = root.findall(".//bnr:Rate", ns)
                for rate in rates:
                    if rate.get('currency') == self._currency:
                        try:
                            self._state = float(rate.text)
                            self._available = True
                            self._multiplier = int(rate.get('multiplier', str(DEFAULT_MULTIPLIER)))
                            self._last_success_update = datetime.now()
                            return
                        except Exception as error:
                            raise BNRRateParseError(f"Failed to convert rate: {error}")

                self._available = False
                raise BNRRateCurrencyError(f"Currency {self._currency} not found")

            except (BNRRateConnectionError, BNRRateParseError, BNRRateCurrencyError) as error:
                self._available = False
                _LOGGER.error(f"[Attempt {attempt}/{BNR_MAX_RETRIES}] {error}")
                if attempt < BNR_MAX_RETRIES:
                    await sleep(BNR_RETRY_INTERVAL)
                else:
                    break
