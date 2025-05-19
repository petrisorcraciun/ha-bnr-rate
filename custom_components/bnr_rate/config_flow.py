import voluptuous as vol
from homeassistant import config_entries
from homeassistant.const import CONF_NAME
from .const import DOMAIN, AVAILABLE_CURRENCIES, DEFAULT_NAME, DEFAULT_CURRENCY

class BNRRateConfigFlow(config_entries.ConfigFlow, domain=DOMAIN):
    async def async_step_user(self, user_input=None):
        errors = {}
        if user_input is not None:
            return self.async_create_entry(title=user_input[CONF_NAME], data=user_input)

        return self.async_show_form(
            step_id="user",
            data_schema=vol.Schema({
                vol.Required(CONF_NAME, default=DEFAULT_NAME): str,
                vol.Required("currency", default=DEFAULT_CURRENCY): vol.In(AVAILABLE_CURRENCIES),
            }),
            errors=errors,
        )
