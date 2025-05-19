from homeassistant.core import HomeAssistant
from homeassistant.config_entries import ConfigEntry
from homeassistant.helpers.typing import ConfigType

DOMAIN = "bnr_rate"

async def async_setup(hass: HomeAssistant, config: ConfigType):
    return True

async def async_setup_entry(hass: HomeAssistant, entry: ConfigEntry):
    await hass.config_entries.async_forward_entry_setups(entry, ["sensor"])
    return True

async def async_unload_entry(hass: HomeAssistant, entry: ConfigEntry):
    unload_ok = await hass.config_entries.async_forward_entry_unload(entry, "sensor")
    return unload_ok
